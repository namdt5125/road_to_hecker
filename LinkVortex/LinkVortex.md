# LinkVortex

<img width="1340" height="774" alt="image" src="https://github.com/user-attachments/assets/8e7b4f10-6f59-4bfe-a52a-6faf08255815" />

Tôi sử dụng `nmap -sV 10.10.11.47` để scan port của địa chỉ ip đó và ra 2 port là 80 và 22 lần lượt là http và ssh:

<img width="993" height="294" alt="image" src="https://github.com/user-attachments/assets/bcdf627b-00f7-41af-81be-6a63ff7fe06b" />

Truy cập vào http của địa chỉ ip `10.10.11.47` thông qua trình duyệt thì có website như này:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/9a3e9616-0ffd-4486-92be-9bab6e4fde68" />

Sử dụng extension thì tôi biết được trang web này sử dụng công nghệ `Ghost 5.58`:

<img width="1798" height="758" alt="image" src="https://github.com/user-attachments/assets/77fda519-9e45-4f43-bc6c-60a786a66045" />

Search thì ra được `CVE-2023-40028` là [Ghost Arbitrary File Read Exploit](https://github.com/0xDTC/Ghost-5.58-Arbitrary-File-Read-CVE-2023-40028) 

<img width="1441" height="879" alt="image" src="https://github.com/user-attachments/assets/56c323b6-2c83-48ec-80dc-c114f0794d1d" />

Vấn đề ở đây là không có username(email) và password để khai thác nên tôi tiếp tục recon, nếu để ý thì có thể thấy tất cả các bài đăng trên trang web này đều do username admin đăng nên khả năng sẽ phải tìm tài khoản 
của admin:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/30fea9d3-0b93-497a-992e-77241b7f19f0" />

<img width="1659" height="967" alt="image" src="https://github.com/user-attachments/assets/3e435521-5bc3-4cda-ade7-de59ae9e0b13" />

Sau khi fuzz directory và subdomain thì directory không ra gì đáng chú ý lắm, subdomain thì ra được `http://dev.linkvortex.htb/` 
```
ffuf -u http://10.10.11.47/ -H 'Host: FUZZ.linkvortex.htb' -w subdomains-top1mil-20000.txt -mc 200,301,302,307,401,403 -ac -t 100 -timeout 2 -rate 50
```
<img width="1810" height="759" alt="image" src="https://github.com/user-attachments/assets/cd4bc885-c418-454d-9d10-226b3cb4fc37" />

Giao diện của website là launching soon, không có gì để tương tác, tiếp tục fuzz thì ra được `.git` 
```
ffuf -u "http://dev.linkvortex.htb/FUZZ" -w namdt_wordlist_1.txt
```
<img width="1063" height="898" alt="image" src="https://github.com/user-attachments/assets/f232099f-b321-4a8f-81dc-100c9dbe9487" />

Có vẻ developer đã không config cẩn thận dẫn đến lộ `.git`, sử dụng tool [git-dumper](https://github.com/arthaud/git-dumper) để lấy src code về:

<img width="1051" height="495" alt="image" src="https://github.com/user-attachments/assets/0e8fa969-0f2a-4c22-a592-5e5663417924" />

Check qua lịch sử commit thì không có gì giá trị lắm, check src code thì mật khẩu admin dùng để test nằm ở file `ghost/core/test/regression/api/admin/authentication.test.js`:

<img width="1545" height="912" alt="image" src="https://github.com/user-attachments/assets/3b2a0d40-bd53-40ef-bd2e-4387f880e3e5" />

Tôi thử với email và mật khẩu trong src nhưng lại không được:

<img width="916" height="658" alt="image" src="https://github.com/user-attachments/assets/ff1cc298-47f6-453c-ad36-21894ca8783f" />

Sau khi thử 1 đống email và cuối cùng cũng được với email `admin@linkvortex.htb` và mật khẩu là `OctopiFociPilfer45`:

<img width="870" height="678" alt="image" src="https://github.com/user-attachments/assets/11bf31d1-5a39-4f6d-8fab-ca1c3a07ca87" />

Vậy là đã đăng nhập vào được dashboard:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/aae73c8e-a132-4abf-840a-1a3bf5c59d3d" />

Quay lại với `Ghost Arbitrary File Read Exploit (CVE-2023-40028)`, đã có đủ thông tin để khai thác:

<img width="1560" height="679" alt="image" src="https://github.com/user-attachments/assets/096f1f45-caf0-4379-88a3-b384b6df395d" />

Lỗ hổng này nằm ở upload file zip, sử dụng symlink để đọc được file trong server, tiếp theo thì file nên đọc là các file config vì có thể chứa thông tin nhạy cảm trong đó

Nếu đọc nội dung trong file `Dockerfile.ghost` thì có đường dẫn đến file `config.production.json` và vị trí ở `/var/lib/ghost/config.production.json`:

<img width="1571" height="912" alt="image" src="https://github.com/user-attachments/assets/62970ba0-8921-4ddb-bb93-8d5e3ab2b16b" />

Lấy được tài khoản của smtp với username là `bob@linkvortex.htb` và mật khẩu là `fibber-talented-worth`:

<img width="1475" height="901" alt="image" src="https://github.com/user-attachments/assets/83fea2e6-d75a-4c40-b731-a1c9e8b11a1c" />

Nhưng khi quét port thì không ra port của smtp, tôi thử ssh vào với user là `bob` và password là `fibber-talented-worth` vì có khả năng bob để cùng 1 mật khẩu, tôi thử và được:

<img width="1245" height="396" alt="image" src="https://github.com/user-attachments/assets/ae109692-f768-4590-9852-353e54aa74f6" />

Tôi thử `sudo -l` thì ra được 1 đoạn script có thể chạy mà không yêu cầu mật khẩu của root:

<img width="1618" height="174" alt="image" src="https://github.com/user-attachments/assets/ad455b1c-2244-440c-bbf9-6fe89ba5dd5a" />

Mở file `/opt/ghost/clean_symlink.sh` thì có nội dung như sau:  
```
#!/bin/bash

QUAR_DIR="/var/quarantined"

if [ -z $CHECK_CONTENT ];then
  CHECK_CONTENT=false
fi

LINK=$1

if ! [[ "$LINK" =~ \.png$ ]]; then
  /usr/bin/echo "! First argument must be a png file !"
  exit 2
fi

if /usr/bin/sudo /usr/bin/test -L $LINK;then
  LINK_NAME=$(/usr/bin/basename $LINK)
  LINK_TARGET=$(/usr/bin/readlink $LINK)
  if /usr/bin/echo "$LINK_TARGET" | /usr/bin/grep -Eq '(etc|root)';then
    /usr/bin/echo "! Trying to read critical files, removing link [ $LINK ] !"
    /usr/bin/unlink $LINK
  else
    /usr/bin/echo "Link found [ $LINK ] , moving it to quarantine"
    /usr/bin/mv $LINK $QUAR_DIR/
    if $CHECK_CONTENT;then
      /usr/bin/echo "Content:"
      /usr/bin/cat $QUAR_DIR/$LINK_NAME 2>/dev/null
    fi
  fi
fi
```
Đoạn script check file có đuôi png xem có phải là symlink trỏ tới file trong thư mục `etc` hoặc `root` không, nếu có thì xóa, nếu không thì di chuyển vào `/var/quarantined`

Vấn đề của đoạn script nằm ở biến `CHECK_CONTENT` , biến này không được khai báo trong đoạn script, có thể thay đổi được giá trị của biến, vấn đề tiếp tục xảy ra ở `if $CHECK_CONTENT;then`, dẫn đến có 2 cách 
để leo quyền:

### Cách leo quyền 1: Lợi dụng việc kiểm soát `CHECK_CONTENT` để đọc file trong thư mục nhạy cảm như root hoặc etc:

Đầu tiên thì tôi tạo 2 cái symlink, cái đầu tiên để trỏ tới file nhạy cảm cần đọc, cái thứ 2 là trung gian:

```
ln -sf /root/root.txt link1
ln -sf /home/bob/link1 link2.png
```

<img width="831" height="611" alt="image" src="https://github.com/user-attachments/assets/a5dd2644-7a38-4935-974c-620a18cafd28" />

Để đọc được nội dung file thì chỉ cần chỉnh biến `CHECK_CONTENT` thành true là ok:
```
export CHECK_CONTENT=true
sudo /usr/bin/bash /opt/ghost/clean_symlink.sh link2.png
```
<img width="1601" height="673" alt="image" src="https://github.com/user-attachments/assets/04030629-48f8-4a9a-9ad2-f7ddc0b87d8f" />

Vậy là có thể đọc được các file trong root bao gồm cả file ssh key

Chốt lại là do biến `CHECK_CONTENT` không được khai báo trong đoạn script, dẫn đến người dùng có thể thay đổi giá trị của nó, việc kiểm tra symlink cũng chưa chặt chẽ khi có thể sử dụng symlink trung gian để đọc

### Cách leo quyền 2: Lợi dụng lỗi logic ở if $CHECK_CONTENT;then

Đầu tiên tôi tạo 1 symlink trỏ bừa đến 1 cái gì đấy `ln -sf /lmao lmao.png`

Sau đó chỉnh biến `CHECK_CONTENT=bash` và chạy `sudo /usr/bin/bash /opt/ghost/clean_symlink.sh lmao.png` là lên thẳng root

<img width="853" height="773" alt="image" src="https://github.com/user-attachments/assets/e6c431c4-6834-45e1-bb4d-3e1e791d3e31" />

Vấn đề do `if $CHECK_CONTENT;then` không được so sánh hay kiểm tra rõ ràng, dẫn đến shell hiểu `$CHECK_CONTENT` như một lệnh để chạy khi truyền `bash` vào, và script này lại đang chạy dưới quyền root nên 
có thể thực thi các lệnh dưới quyền root
