import requests

url = 'https://euipo.europa.eu/eSearch/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36',
}
res = requests.get(url=url, headers=headers)
hd = res.headers.items()
print(hd)
