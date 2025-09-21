# MonitorsThree

<img width="1462" height="647" alt="image" src="https://github.com/user-attachments/assets/a05c0523-cf1e-4182-8aa4-819d8dd4904d" />

Đầu tiên thì tôi dùng nmap để scan các port thì ra được 2 port gồm 22 và 80 là đang mở:

```
❯ sudo nmap -sV 10.10.11.30
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-21 11:50 +0700
Nmap scan report for monitorsthree.htb (10.10.11.30)
Host is up (0.037s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE    SERVICE VERSION
22/tcp   open     ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp   open     http    nginx 1.18.0 (Ubuntu)
8084/tcp filtered websnp
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.30 seconds
```

Giao diện trang web sau khi truy cập bằng trình duyệt:

<img width="1873" height="944" alt="image" src="https://github.com/user-attachments/assets/f183c846-7cd9-43ed-ab0f-fa4442bd21bf" />

Bằng cách fuzz subdomain thì tôi tìm được thêm `http://cacti.monitorsthree.htb/`:

<img width="1870" height="901" alt="image" src="https://github.com/user-attachments/assets/82a8975c-1187-4ce2-a14e-d3579dcb2926" />

Ở đây biết được website sử dụng phiên bản `1.2.26` ở `http://cacti.monitorsthree.htb/` và tìm được [CVE-2024-25641](https://github.com/cacti/cacti/security/advisories/GHSA-7cmj-g5qc-pj88)

CVE này liên quan đến upload tệp `.xml.gz` nhưng cần phải đăng nhập vào tài khoản của user có quyền upload package.

Ở chức năng `forgot_password.php` khi tôi nhập `test'` thì có xuất hiện lỗi:

<img width="1653" height="901" alt="image" src="https://github.com/user-attachments/assets/d2875902-e6fd-4826-9455-fe0bcd61bada" />

Có vẻ như xảy ra sqli, kiểm chứng thêm bằng `admin' AND '1'='1`:

<img width="711" height="633" alt="image" src="https://github.com/user-attachments/assets/4c37fd39-1cbb-475c-b021-38aa8b588c9d" />

Tôi viết tạm đoạn script để xử lý sqli base error này và lấy được hash mật khẩu của admin:

<img width="1062" height="899" alt="image" src="https://github.com/user-attachments/assets/27979426-fa07-4cca-8f8c-90497489a2db" />










































