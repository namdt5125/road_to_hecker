# UltraTech

<img width="1539" height="315" alt="image" src="https://github.com/user-attachments/assets/c25ff8e9-486d-4eb6-b09f-09db9f7adeb9" />

Target ở đây là `10.64.177.169`, đầu tiên thì tôi sử dụng nmap để scan các port có trên server:

```
sudo nmap 10.64.177.169 -Pn -sV -sC -p- --min-rate=200 -T 4 -oN mediumlab -v
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.5
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 84:6e:12:4c:f0:83:eb:75:3e:f5:67:ba:7e:3b:0a:32 (RSA)
|   256 8a:f0:2e:b2:f0:28:33:9f:f1:db:44:5e:2c:84:48:ad (ECDSA)
|_  256 aa:21:c2:1f:6f:2f:3b:af:7b:66:f6:fe:56:06:d5:d8 (ED25519)
8081/tcp  open  http    Node.js Express framework
|_http-cors: HEAD GET POST PUT DELETE PATCH
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
31331/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 15C1B7515662078EF4B5C724E2927A96
|_http-title: UltraTech - The best of technology (AI, FinTech, Big Data)
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET POST OPTIONS HEAD
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

Ở đây có 2 port gồm 8081 và 31331 là chạy web, fuzzing thì ra được:

```
ffuf -u "http://10.64.177.169:8081/FUZZ" -w ~/wordlist/super_mega_wordlist.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.64.177.169:8081/FUZZ
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/super_mega_wordlist.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

auth                    [Status: 200, Size: 39, Words: 8, Lines: 1, Duration: 227ms]
Auth                    [Status: 200, Size: 39, Words: 8, Lines: 1, Duration: 228ms]
ping                    [Status: 500, Size: 1094, Words: 52, Lines: 11, Duration: 230ms]
?view=log               [Status: 200, Size: 20, Words: 3, Lines: 1, Duration: 226ms]
?wsdl                   [Status: 200, Size: 20, Words: 3, Lines: 1, Duration: 226ms]
```

Tiếp theo thì tôi thử tìm kiếm ở `http://10.64.177.169:31331/` thì có xuất hiện `robots.txt`, trong đó thì lại có `utech_sitemap.txt`:

<img width="560" height="191" alt="image" src="https://github.com/user-attachments/assets/9bde7e52-06f4-4eb5-b753-bd85c4c6f900" />

Khi truy cập vào `http://10.64.177.169:31331/partners.html` thì có xuất hiện chỗ để login:

<img width="693" height="459" alt="image" src="https://github.com/user-attachments/assets/b86fa52b-5732-4080-845b-071d246cac7d" />

Trong quá trình truy cập vào `http://10.64.177.169:31331/partners.html` thì có xuất hiện `/ping?ip=10.64.177.169`:

<img width="972" height="650" alt="image" src="https://github.com/user-attachments/assets/7ead40f5-e040-4fcd-87b2-d3f97800be1d" />

Ở đây thì có xuất hiện cmdi:

<img width="984" height="499" alt="image" src="https://github.com/user-attachments/assets/71209b42-701d-40db-afcf-efef0e6f7991" />

Tôi tìm được hash của 2 user là `admin` và `r00t`:

<img width="990" height="481" alt="image" src="https://github.com/user-attachments/assets/693c0009-70e4-4808-8b7b-9ee003a2c20f" />

<img width="1075" height="396" alt="image" src="https://github.com/user-attachments/assets/bbd9b6d5-b0bc-4706-9cd1-c1ecc25a1a48" />

Tôi thử dùng để ssh vào thì được:

<img width="844" height="675" alt="image" src="https://github.com/user-attachments/assets/7ed0351d-0b28-4bcc-a059-dd848b6301fc" />

Kiểm tra thì có container đang chạy ở docker, check log thì có xuất hiện ssh key của root:

<img width="1123" height="971" alt="image" src="https://github.com/user-attachments/assets/7541b3e5-dd64-48f6-9323-fbeea536f9ad" />

<img width="962" height="968" alt="image" src="https://github.com/user-attachments/assets/617e5ba5-cd49-4e06-adf8-b502927d233d" />








