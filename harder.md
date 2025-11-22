# harder

<img width="1425" height="331" alt="image" src="https://github.com/user-attachments/assets/b2af94ed-ca42-4f49-a0c1-01eb359eff0e" />

Target là `10.65.153.67`, tôi sử dụng nmap để kiểm tra qua các port đang mở và có port 80 và 22:

```
sudo nmap -Pn --min-rate=200 -T4 -v 10.65.153.67
Starting Nmap 7.98 ( https://nmap.org ) at 2025-11-22 15:38 +0700
Initiating Parallel DNS resolution of 1 host. at 15:38
Completed Parallel DNS resolution of 1 host. at 15:38, 0.00s elapsed
Initiating SYN Stealth Scan at 15:38
Scanning 10.65.153.67 (10.65.153.67) [1000 ports]
Discovered open port 22/tcp on 10.65.153.67
Discovered open port 80/tcp on 10.65.153.67
Completed SYN Stealth Scan at 15:38, 4.55s elapsed (1000 total ports)
Nmap scan report for 10.65.153.67 (10.65.153.67)
Host is up (0.23s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

Tôi truy cập vào trang web nhưng ở đây chả có gì cả, fuzz endpoint và crawl không thấy gì hết:

<img width="1908" height="1014" alt="image" src="https://github.com/user-attachments/assets/3ab3d573-8674-4595-b614-8f680d5c47a6" />

Để ý trong response thì có xuất hiện domain:

<img width="926" height="838" alt="image" src="https://github.com/user-attachments/assets/f8636ca0-4950-4666-9a35-0845ea2ac038" />

Tôi trỏ domain vào địa chỉ ip và dùng curl thì hiện ra form để đăng nhập:

<img width="1904" height="970" alt="image" src="https://github.com/user-attachments/assets/60861404-463a-4db0-a2e8-f9603d411a4f" />

Tôi thử với cred mặc định là `admin:admin` thì hiển thị như này:

<img width="1912" height="976" alt="image" src="https://github.com/user-attachments/assets/c011f7b6-0bb5-4583-a8da-a5cb508e45c8" />

Và có thể thấy website này bị lộ .git:

<img width="1776" height="795" alt="image" src="https://github.com/user-attachments/assets/3930c5e8-27ed-4101-86e1-d3544cbecb8a" />

Sử dụng `git-dumper http://pwd.harder.local/ pwd_harder_local` để lấy src code về, sau khi lấy về tôi check log thì không có gì đặc biệt, check code thì có 1 số file như sau (bỏ file hm.php và secret.php đi, 2 file đấy tôi tạo để test):

<img width="928" height="433" alt="image" src="https://github.com/user-attachments/assets/8831b2a5-3943-4094-b495-f3b4a42eb820" />

Ở index.php thì có các file `auth.php`, `hmac.php`, `credentials.php`. Trong đó thì qua được `auth.php` nhờ `admin:admin` rồi, còn mỗi `hmac.php` và `credentials.php`, nhưng `credentials.php` lại không có trong src code:

<img width="831" height="491" alt="image" src="https://github.com/user-attachments/assets/c0b647ef-85aa-4b59-bc35-ae8f78fcb659" />

Còn ở `hmac.php` thì lấy 2 param gồm n, h và host, sau đó lấy `$secret` từ `secret.php` ra, sử dụng `hash_hmac` với data là n (nếu có) và key là `$secret`, tiếp theo là `hash_hmac` với data là host và key là `$secret`, cuối cùng là so sánh h với hm sau khi được tính toán xong:

<img width="687" height="441" alt="image" src="https://github.com/user-attachments/assets/59def49a-f571-42e7-8156-1358fa4c99ea" />

Ở đây thì tôi có tạo file là `hm.php` để mô phỏng lại và in ra màn hình

```
<?php

$h = "0a857c7e169318a6e419f21c00dc6d9517da664749c1dfa93c7473738220e483" ;
$host = "test.com" ;
$n = "test" ;


if (empty($h) || empty($host)) {
   echo "missing get parameter";
   die();
}
require("secret.php");
if (isset($n)) {
   $secret = hash_hmac('sha256', $n, key: $secret);
   echo $secret . "\n";
}

$hm = hash_hmac('sha256', $host, false);
echo $hm . "\n";
if ($hm !== $h){
  echo "extra security check failed";
  die();
}
?>
```

Ở đoạn `$hm = hash_hmac('sha256', $host, false);` thì muốn kiểm soát được phải thay đổi key của nó là false hoặc "", mà trước đó có kiểm tra xem $n có không, $n ở đây lại là kiểu String, ý tưởng ở đây là thay đổi kiểu giá trị của $n dẫn đến đoạn `$secret = hash_hmac('sha256', $n, key: $secret);` xảy ra lỗi và trở thành false

Ở đây thì là ép kiểu sang array trên param, có thể tham khảo ở [đây](https://security.stackexchange.com/questions/180265/array-in-http-get-post-requests):

<img width="949" height="265" alt="image" src="https://github.com/user-attachments/assets/fed1ec0a-3d7c-41f6-9331-c6d14dcb0328" />

Lúc này thì xuất hiện subdomain khác và cred khác:

<img width="1875" height="922" alt="image" src="https://github.com/user-attachments/assets/a4c827c5-ba1a-4ce7-b174-dd13b31116d3" />

Khi truy cập vào `http://shell.harder.local` thì hiển thị ra cái này:

<img width="1910" height="901" alt="image" src="https://github.com/user-attachments/assets/1fcc69e6-497f-4adb-a174-0ecf4ee4e6eb" />

Tôi thêm `X-Forwarded-For: 10.10.10.10` vào 

<img width="1911" height="883" alt="image" src="https://github.com/user-attachments/assets/184e70ba-ffe0-45a8-af28-733bf2dce08e" />

<img width="1885" height="686" alt="image" src="https://github.com/user-attachments/assets/df194a2d-d992-435a-8658-29379a1cef30" />

Kiểm tra trong `/etc/periodic/` thì có chứa script được đặt lịch chạy và nó lại chứa cred của user evs:

<img width="1910" height="932" alt="image" src="https://github.com/user-attachments/assets/5866cb6a-8df3-4441-9cd2-600e7fde92d8" />










