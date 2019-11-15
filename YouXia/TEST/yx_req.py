import requests

url = 'http://so.ali213.net/s/s?sub=91&page=1&keyword=%E8%8B%B1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}

a = requests.get(url=url, headers=headers)
pass
