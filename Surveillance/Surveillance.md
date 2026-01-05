<img width="1913" height="1007" alt="image" src="https://github.com/user-attachments/assets/3cf290a7-1d31-483b-b4b8-1f84453743f9" /># Surveillance

<img width="1441" height="543" alt="image" src="https://github.com/user-attachments/assets/0b59b061-84eb-4ab2-943b-5c64c761808e" />

Target là `10.129.230.42`, tôi dùng nmap để scan port:

```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 96:07:1c:c6:77:3e:07:a0:cc:6f:24:19:74:4d:57:0b (ECDSA)
|_  256 0b:a4:c0:cf:e2:3b:95:ae:f6:f5:df:7d:0c:88:d6:ce (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://surveillance.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Tôi dùng gospider để lấy các link có trong website thì thấy quả link dẫn đến `Craft CMS` phiên bản `4.4.14`:

```
gospider -s "http://surveillance.htb/" -o output -c 10 -d 1
```

<img width="979" height="816" alt="image" src="https://github.com/user-attachments/assets/febd6bb1-3057-4ae9-a235-a3bed640986f" />

Tôi tìm được CVE liên quan đến phiên bản này là CVE_2023_41892:

<img width="983" height="887" alt="image" src="https://github.com/user-attachments/assets/2d068e35-ed95-42f4-817f-5201bd9234b8" />

Ở đây tôi có mở file `.env` và sử dụng cred để truy cập vào mysql, tìm được mật khẩu nhưng không crack được:

<img width="863" height="656" alt="image" src="https://github.com/user-attachments/assets/263d6a93-e2f6-4da8-b5cf-5234bce372ec" />

Tôi mở src code và thấy trong đó có file nén `storage/backups/surveillance--2023-10-17-202801--v4.4.14.sql/surveillance--2023-10-17-202801--v4.4.14.sql` tôi giải nén ra và ngồi xem thì có password được hash, crack ra được mật khẩu của matthew:

<img width="1752" height="870" alt="image" src="https://github.com/user-attachments/assets/f88d2476-04ef-4c5d-b006-9f688ff48866" />

Và có port 8080 đang được mở bên trong

```
ssh -L 1234:localhost:8080 matthew@10.129.230.42
```

Tôi tìm được src code của website đang chạy trên 8080:

<img width="1211" height="434" alt="image" src="https://github.com/user-attachments/assets/402c7c24-96bd-4c30-b5ac-dc0e8b61f01a" />

Dùng mật khẩu của matthew thì login vào được:

<img width="950" height="1022" alt="image" src="https://github.com/user-attachments/assets/c3cc06a8-4b85-4fe7-a420-3f066f362cf4" />

Tôi check trong src code thì được version của nó:

<img width="1548" height="1016" alt="image" src="https://github.com/user-attachments/assets/a1859cad-b11e-49b1-bdc9-45c6496eb144" />

Tôi tìm được [CVE-2023-26035](https://github.com/heapbytes/CVE-2023-26035):

<img width="1847" height="428" alt="image" src="https://github.com/user-attachments/assets/dd383a68-0eda-4c1f-becf-3900b97c9eba" />

Và rce được vào với user là `zoneminder` và ở đó có `(ALL : ALL) NOPASSWD: /usr/bin/zm[a-zA-Z]*.pl *`



