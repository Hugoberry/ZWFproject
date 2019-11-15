import requests

url = "http://zhaopin.baidu.com/company?query=4debc0f405c93ce495564c8f4bce6b99"
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }

a = requests.get(url=url, headers=headers)
pass
