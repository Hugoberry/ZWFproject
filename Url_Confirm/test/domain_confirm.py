import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/70.0.3538.67 Safari/537.36'
}

text = requests.post('http://icp.chinaz.com/gvv.com', headers=headers).text
# print(text)
# sth = re.compile(r'<span>主办单位名称</span><p>(.*?)</p></li>').findall(text)[0]
# print(sth)
a = re.compile(r'<p id="err" class="tc col-red fz18 YaHei pb20">未备案或者备案取消，获取最新数据请<a href="'
                 r'javascript:" class="updateByVcode">\((.*?)\)</a></p>').findall(text)
if a:
    print('======================')
