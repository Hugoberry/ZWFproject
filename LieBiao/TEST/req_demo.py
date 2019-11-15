import requests


url = 'http://beijing.liebiao.com/gongshangzhuce/478001323.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
text = requests.get(url=url, headers=headers)

pass
