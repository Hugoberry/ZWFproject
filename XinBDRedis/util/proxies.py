"""工具文件"""
from telnetlib import Telnet
import json
import requests
import time
import random


# 检测代理 IP 是否可用
def check_proxies(ip, port):
    try:
        Telnet().open(ip, port, timeout=2)
        return True
    except Exception:
        return False


class Proxies(object):
    def __init__(self, client):
        self.proxies_key = "proxies_key"
        self.proxies_api = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=5b817f58bea74822a6c369e567e278bc&orderno=YZ201810154990ve5V4h&returnType=2&count=1"
        self.client = client
        self.default_encode = json.JSONEncoder().encode
        self.default_decode = json.JSONDecoder().decode
        self.get_proxies_for_api() if not self.client.exists(self.proxies_key) else 0  # 执行一次放入url

    # 0. 获取代理
    def get_proxies_for_api(self):
        # api return value like this {"port":"49572","ip":"223.242.246.201"}
        while True:
            result = json.loads(requests.get(self.proxies_api).text).get("RESULT")[0]
            if result and isinstance(result, dict):
                f = check_proxies(**result)
                if f:
                    self.put_proxies(result)
                    return
            time.sleep(random.random() * 3)

    # 1. 代理入 redis
    def put_proxies(self, proxies_value):
        self.client.lpush(self.proxies_key, self.default_encode(proxies_value))

    # 2. 代理出 redis
    def get_proxies(self, update=False):
        if update:
            self.update_proxies()
        return self.default_decode(self.client.lindex(self.proxies_key, 0).decode("utf-8"))

    # 3. 删除代理
    def delete_proxies(self):
        self.client.delete(self.proxies_key)

    # 4. 更新代理
    def update_proxies(self):
        self.delete_proxies()
        self.get_proxies_for_api()

