<img width="885" height="845" alt="image" src="https://github.com/user-attachments/assets/c4591ed2-3a68-418d-8183-1fcbe5380ba7" /># Road

<img width="1106" height="323" alt="image" src="https://github.com/user-attachments/assets/0ce712b8-4486-4977-af0f-beaac61b0581" />

Mục tiêu ở đây là `10.10.89.51`, bắt đầu là tôi scan nhanh qua các port có trên server:

```
sudo nmap 10.10.89.51 -Pn -sV -sC -p- --min-rate=200 -T 4
```

Tôi tìm được 2 port gồm 80 và 22:

<img width="838" height="323" alt="image" src="https://github.com/user-attachments/assets/4b62087b-65d2-4601-8602-e60f01e369a0" />

Truy cập vào port 80 thì trả về giao diện này:

<img width="1897" height="1020" alt="image" src="https://github.com/user-attachments/assets/9576095a-51b0-4bbb-8c1b-3a712cfdd3bd" />

Fuzzing qua thì không có gì đặc sắc, dùng gospider check qua các đường dẫn thì có cái `http://10.10.89.51/v2/admin/login.html`:

<img width="819" height="589" alt="image" src="https://github.com/user-attachments/assets/002edf3d-be3a-4d12-b471-62e7c6584a43" />

<img width="1904" height="961" alt="image" src="https://github.com/user-attachments/assets/4866ab79-2925-4115-8f02-51a273190296" />

Tôi thử bruteforce và sqli nhưng có vẻ không được, tôi đi đăng kí tạm tài khoản mới và giao diện sau khi login:

<img width="1911" height="799" alt="image" src="https://github.com/user-attachments/assets/88fbb67a-d9f0-4304-a821-c36788b8047b" />

1 số tính năng chính là upload ảnh, có vẻ nó sẽ dính file upload do sử dụng php, nhưng mà chỉ có admin mới upload được:

<img width="1910" height="1022" alt="image" src="https://github.com/user-attachments/assets/e48819d4-9364-418a-9d0c-468b763d1bf1" />

Tính năng search thì chưa có:

<img width="766" height="189" alt="image" src="https://github.com/user-attachments/assets/7919a1cf-44d4-42e4-ab50-efa396f05e70" />

Và cuối cùng là tính năng đổi mật khẩu:

<img width="1908" height="761" alt="image" src="https://github.com/user-attachments/assets/68ea6e51-426e-4fc6-8678-a7978f0aee3b" />

Ở tính năng đổi mật khẩu lại có xuất hiện username của tài khoản đang đổi:

<img width="1547" height="994" alt="image" src="https://github.com/user-attachments/assets/4f410dd6-f10e-43f1-bb8e-9e62cb53bd1a" />

Tôi thử tạo 1 tài khoản khác và có thể đổi được mật khẩu của user khác

Để ý kĩ thì tài khoản của admin là `admin@sky.thm`:

<img width="564" height="150" alt="image" src="https://github.com/user-attachments/assets/a54122f0-71da-4f9a-91ce-a479aaa5a252" />

Và tôi đã có thể đăng nhập vào tài khoản của admin:

<img width="1911" height="797" alt="image" src="https://github.com/user-attachments/assets/e1964344-dc25-463e-8e65-2886badf75a2" />

Và tôi đã upload ảnh thành công:

<img width="1553" height="997" alt="image" src="https://github.com/user-attachments/assets/34a4a88f-9231-4856-a110-3c1134e31e5e" />

Dùng các công cụ bình thường thì tôi không tìm thấy, tôi dùng Gemini để check lại cho chắc thì tìm đường dẫn `/v2/profileimages/`:

<img width="897" height="873" alt="image" src="https://github.com/user-attachments/assets/83f8e569-2b2f-4e10-9ad9-3126fe59c5a2" />

<img width="1906" height="953" alt="image" src="https://github.com/user-attachments/assets/b2a448ee-fd4c-4a1d-b909-98069b2fd1b1" />

Tôi thử upload file php và nó thành công:

<img width="1918" height="1055" alt="image" src="https://github.com/user-attachments/assets/465ca7b1-f1f3-4ad3-a70e-0c83d852a548" />

Lúc này thêm reverse shell vào:

<img width="1913" height="1011" alt="image" src="https://github.com/user-attachments/assets/01aeaf57-c4db-4056-b4ed-1a78ebab6418" />

Đọc file `/etc/passwd` thì biết thêm được 1 số thông tin như là server này sử dụng mongodb và mysql, có user là root, ubuntu và webdeveloper:

<img width="949" height="983" alt="image" src="https://github.com/user-attachments/assets/8c65df6a-44ae-41f6-adee-2a50462c5657" />

Bằng cách mở các file liên quan đến truy vấn để login hay gì đó thì tôi tìm được cred của mysql

<img width="939" height="890" alt="image" src="https://github.com/user-attachments/assets/9275361a-4015-4a91-b995-7d52c41c1da7" />

Trong mysql thì tôi có tìm và thấy 1 đoạn hash nhưng không crack bằng wordlist rockyou được nên bỏ qua:

<img width="1895" height="989" alt="image" src="https://github.com/user-attachments/assets/3ca3bf2c-aba1-4894-9b42-34bc0c59e9fe" />

Tôi chuyển sang mongodb thì tìm được cred có vẻ là của webdeveloper:

<img width="1042" height="917" alt="image" src="https://github.com/user-attachments/assets/9a0c3ec3-f24a-4d9e-8270-debb3dae063d" />

Và đã truy cập vào được với user là webdeveloper:

<img width="885" height="845" alt="image" src="https://github.com/user-attachments/assets/a1e0bf0b-9b28-4a44-8eeb-56a4df8df7aa" />





































