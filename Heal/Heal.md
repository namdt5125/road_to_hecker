# Heal

<img width="1450" height="443" alt="image" src="https://github.com/user-attachments/assets/cedabe6c-d8c9-485f-a970-0892caf37859" />

Sử dụng nmap đối với target thì có xuất hiện 2 port gồm 22 và 80:

```
sudo nmap 10.129.6.53 -Pn -sV -sC -p- --min-rate=200 -T 4 -oN mediumlab -v
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 68:af:80:86:6e:61:7e:bf:0b:ea:10:52:d7:7a:94:3d (ECDSA)
|_  256 52:f4:8d:f1:c7:85:b6:6f:c6:5f:b2:db:a6:17:68:ae (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Heal
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-favicon: Unknown favicon MD5: 800D9D6AD40E40173F19D5EE9752AC18
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Truy cập thông qua browser thì xuất hiện giao diện như này:

<img width="1909" height="924" alt="image" src="https://github.com/user-attachments/assets/e6dfe311-025e-4da0-9500-a835fd99b8af" />

Tôi tìm được thêm 2 subdomain là `api.heal.htb` và `take-survey.heal.htb`:

<img width="700" height="358" alt="image" src="https://github.com/user-attachments/assets/fe2d3870-1f65-4941-a6a8-2153dbb6acab" />

Sau khi login thì có xuất hiện cái này, gồm điền form gửi đi và export tải về máy:

<img width="1906" height="962" alt="image" src="https://github.com/user-attachments/assets/9b6d5c68-76e7-480e-ae03-442ea8f0cb6e" />

Ở `/download?filename=f77ef1fb0a52e447ba3b.pdf` có param filename nhận tên file và trả về file đó:

<img width="1907" height="910" alt="image" src="https://github.com/user-attachments/assets/a28d62ae-6427-4bd0-a9d6-81399803499f" />

Tôi thử path traversal và nó được:

<img width="1913" height="825" alt="image" src="https://github.com/user-attachments/assets/9762d213-02a9-4d33-9983-400f45eedc1b" />





















