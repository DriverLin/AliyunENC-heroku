import base64
import hashlib
import json
import os
import threading

import requests
from cryptography.fernet import Fernet


def dec(key, data):
    md5hash = hashlib.md5(key.encode()).hexdigest().encode('utf-8')
    f = Fernet(base64.urlsafe_b64encode(md5hash))
    return f.decrypt(data.encode('utf-8')).decode('utf-8')

token_bin_url = "https://raw.githubusercontent.com/DriverLin/action_ruler/main/aliyunpan/auto_refresh/refresh_token.bin"
response = requests.get(token_bin_url)
refresh_token = dec(os.environ.get("KEY") ,response.text)
deployAliyunWebdavCMD = "aliyundrive-webdav --refresh-token {} -p 8900 --cache-ttl 16 --debug  --upload-buffer-size 4194304".format(refresh_token)

def getThread(port):
    return [
        threading.Thread(target=os.system, args=(deployAliyunWebdavCMD,)),
        threading.Thread(target=os.system, args=(f"./rclone  --config ./rclone.conf         serve http aliyunenc:ADM --addr 0.0.0.0:{port} --read-only",))
    ]

if __name__ == "__main__":
    os.system("chmod 777 ./rclone")
    os.system("pip install aliyundrive-webdav")

    threads = getThread(os.environ.get("PORT"))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
