import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.67 Safari/537.36',
}
url_token = 'https://promotion.aliyun.com/risk/getToken.htm'

token_text = requests.get(url=url_token, headers=headers).text
# print(token_text)
token = json.loads(token_text, encoding='utf-8')['data']
print(token)
url_site = 'https://checkapi.aliyun.com/check/checkdomain?domain={}.{}&command=&token={}&ua=&currency=' \
           '&site=&bid=&_csrf_token='.format('aiqinghai', 'top', token)
site_text = requests.get(url=url_site, headers=headers).text
site = json.loads(site_text, encoding='utf-8')
print(site)
print(type(site))
'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=xiaomi.cn'
