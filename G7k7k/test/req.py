import requests
from lxml import etree

url = 'http://so.7k7k.com/game/%E9%BB%94%E5%86%9CE%E8%B4%B7.htm'
text = requests.get(url=url).text
html = etree.HTML(text)
res_null = html.xpath('//div[@class="s_box"]/div/@class')
print(res_null)
if 'search_null' in res_null:
    print(res_null)
