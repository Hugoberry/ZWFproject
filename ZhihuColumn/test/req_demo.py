import json
import re
# import json
import time

import requests
from lxml import etree

headers = {
    # ':authority': 'www.zhihu.com',
    # ':method': 'GET',
    # ':path': '/api/v4/search_v3?t=topic&q=%E5%B0%8F%E7%B1%B3&correction=1&offset=185&limit=10&show_all_topics=1&search_hash_id=aad2c6db486062cd8e3ee8d74e1380ae',
    # ':scheme': 'https',
    # 'referer': 'https://www.zhihu.com/search?q=%E5%96%9C%E6%B4%8B%E6%B4%8B&type=column',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
}
html = requests.get('https://www.zhihu.com/search?type=column&q=%E5%B0%8F%E7%B1%B3', headers=headers)
tx = html.text
print(tx)
search_hash_id = re.compile(r'&search_hash_id=(.*?)&show_all_topics=').findall(tx)[0]
print(search_hash_id)
raw_html = etree.HTML(tx)
aim = raw_html.xpath('//div[@class="List-item"]/div[@class="ContentItem"]//div[@class="ContentItem-head"]/h2[@class="ContentItem-title"]//span')
print('**************************')
print(aim)
for a in aim:
    print(a.text)
# for i in range(20):
#     ajax_url = 'https://www.zhihu.com/api/v4/search_v3?t=topic&q=%E5%B0%8F%E7%B1%B3&correction=1&offset={}&' \
#                'limit=10&show_all_topics=1&search_hash_id={}'.format(int((i + 1) * 5), search_hash_id)
#     time.sleep(1.5)
#     info = requests.get(ajax_url, headers=headers).content
#     json_info = json.loads(info)
#     print(json_info)
#     print(type(json_info))

# 这段是取第一个五条数据的测试
par = re.compile('<img class="Avatar Avatar--large" width="60" height="60" src="(.*?)" srcSet="(.*?) 2x" alt="(.*?)"/>'
                 '</div></div></a></div><div class="ContentItem-head"><h2 class="ContentItem-title"><div><a class='
                 '"ColumnLink" href="(.*?)" target="_blank"><div class="Popover"><div id="null-toggle" aria-haspopup='
                 '"true" aria-expanded="false" aria-owns="null-content"><span class="Highlight">(.*?)</span></div>'
                 '</div></a></div></h2><div class="ContentItem-meta"><div><div class="RichText ztext SearchItem-meta '
                 'Highlight">(.*?)</div><div class="ContentItem-status"><span class="ContentItem-statusItem '
                 'Search-statusLink">创建者：<span class="UserLink"><div class="Popover"><div id="null-toggle" '
                 'aria-haspopup="true" aria-expanded="false" aria-owns="null-content"><a class="UserLink-link" '
                 'data-za-detail-view-element_name="User" target="_blank" href="(.*?)">(.*?)</a></div></div></span>'
                 '</span><a class="ContentItem-statusItem Search-statusLink" target="_blank" href="(.*?)">(.*?) 关注'
                 '</a><a class="ContentItem-statusItem Search-statusLink" target="_blank" href="(.*?)">(.*?) 文章</a>')
info = par.findall(tx)
for i in info:
    print(i)
