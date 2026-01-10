<img width="1448" height="544" alt="image" src="https://github.com/user-attachments/assets/c5db1bb1-7bb3-4730-b6ea-2d7e6b679e72" />

Target ở đây là `10.10.11.183`, tôi dùng nmap để scan ra 4 port trong đó có 2 port là http:

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 29:dd:8e:d7:17:1e:8e:30:90:87:3c:c6:51:00:7c:75 (RSA)
|   256 80:a4:c5:2e:9a:b1:ec:da:27:64:39:a4:08:97:3b:ef (ECDSA)
|_  256 f5:90:ba:7d:ed:55:cb:70:07:f2:bb:c8:91:93:1b:f6 (ED25519)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-title: Ambassador Development Server
|_http-generator: Hugo 0.94.2
|_http-server-header: Apache/2.4.41 (Ubuntu)
3000/tcp open  http    Grafana http
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
| http-robots.txt: 1 disallowed entry 
|_/
| http-title: Grafana
|_Requested resource was /login
|_http-favicon: Unknown favicon MD5: 279F94A1965D11699C4E33714AE33492
|_http-trane-info: Problem with XML parsing of /evox/about
3306/tcp open  mysql   MySQL 8.0.30-0ubuntu0.20.04.2
| mysql-info: 
|   Protocol: 10
|   Version: 8.0.30-0ubuntu0.20.04.2
|   Thread ID: 9
|   Capabilities flags: 65535
|   Some Capabilities: LongColumnFlag, InteractiveClient, Speaks41ProtocolNew, SupportsCompression, Support41Auth, Speaks41ProtocolOld, SupportsTransactions, IgnoreSigpipes, IgnoreSpaceBeforeParenthesis, LongPassword, DontAllowDatabaseTableColumn, SwitchToSSLAfterHandshake, ODBCClient, FoundRows, SupportsLoadDataLocal, ConnectWithDatabase, SupportsMultipleStatments, SupportsMultipleResults, SupportsAuthPlugins
|   Status: Autocommit
|   Salt: A}nir)\x0Ec\x15UD\x1D\x14\x15d2 ,\x06{
|_  Auth Plugin Name: caching_sha2_password
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Đây là 2 giao diện của trang web:

<img width="1903" height="999" alt="image" src="https://github.com/user-attachments/assets/b3dae8e3-2a53-4847-b346-9511ca9a6b37" />

Ở phần forgot password thì hiển thị ra phiên bản của Grafana là `v8.2.0`:

<img width="946" height="695" alt="image" src="https://github.com/user-attachments/assets/4fbec20a-7390-4796-8949-c5915a53f3a3" />

Ở đây tôi tôi tìm được [CVE-2021-43798](https://github.com/pedrohavay/exploit-grafana-CVE-2021-43798?tab=readme-ov-file) path traversal:

<img width="1529" height="891" alt="image" src="https://github.com/user-attachments/assets/ee6db237-1dbb-477d-a8a5-023c54fc46c0" />

Tôi thành công đọc được path traversal, tôi tìm được 1 số path thường gặp trong server và đọc:

<img width="687" height="375" alt="image" src="https://github.com/user-attachments/assets/401fe792-1c63-4971-8d73-3b6d3ca254fa" />

Tìm được 2 file nhạy cảm là `/..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fvar/lib/grafana/grafana.db` và `/..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc/grafana/grafana.ini`:

<img width="1525" height="833" alt="image" src="https://github.com/user-attachments/assets/45e93ea1-7afc-46db-97b0-6cc58dcc090b" />

<img width="1524" height="815" alt="image" src="https://github.com/user-attachments/assets/a6452bc4-5358-4d5d-8e28-5718a01cc751" />

Và tìm được thêm password của developer, check trong `/etc/passwd` thì có user này:

<img width="1682" height="1010" alt="image" src="https://github.com/user-attachments/assets/e44cbd9b-45a2-4640-9a81-559ebf888501" />

Vậy là truy cập vào được user developer:

<img width="915" height="872" alt="image" src="https://github.com/user-attachments/assets/43b4425d-e758-40e4-b9f1-4a9bd7ea5fde" />

Tôi dùng `ps auxww` và thấy có consul được chạy dược vào config file `/etc/consul.d/consul.hcl`

<img width="1887" height="962" alt="image" src="https://github.com/user-attachments/assets/b70ea9cd-1476-469c-81cf-f0776e6e674d" />

Check trong `/opt/my-app/` thì thấy có `.git` 

<img width="632" height="633" alt="image" src="https://github.com/user-attachments/assets/5710ab71-d3c2-47ee-9a5f-22df5063cead" />

Tôi tìm được token trong git log:

<img width="1057" height="911" alt="image" src="https://github.com/user-attachments/assets/85c0caa9-798d-4017-9ca6-a067fad72713" />

Có thể thấy thư mục `/etc/consul.d/config.d` có quyền write và exe nhưng không có quyền read nên không thể đọc được file trong đấy 

<img width="589" height="260" alt="image" src="https://github.com/user-attachments/assets/c65014c7-ae03-4519-965c-983e3d0b49db" />

Tôi upload file execute.hcl lên `/etc/consul.d/config.d` server:

<img width="1898" height="457" alt="image" src="https://github.com/user-attachments/assets/b4713e74-1037-4bda-b925-3bc5ade4fe0c" />

<img width="877" height="309" alt="image" src="https://github.com/user-attachments/assets/a2bfcb0e-7227-4cf2-8c74-2748ec70a9e3" />

