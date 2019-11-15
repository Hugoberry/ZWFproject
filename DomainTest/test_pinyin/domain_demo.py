import requests
import re

domain_str = 'baidu.xyz'
domain_url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain='
url = domain_url + domain_str
text = requests.get(url=url).text
# print(text)
return_code = re.compile('<returncode>(.*)</returncode>').findall(text)[0]
return_key = re.compile('<key>(.*)</key>').findall(text)[0]
return_original = re.compile('<original>(.*)</original>').findall(text)[0]
print(return_code)
print(return_key)
print(return_original)
