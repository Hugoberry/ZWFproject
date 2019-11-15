# 由于第三方包fake_useragent 出现故障， 无法正常访问
# 为了解决这个问题找到了请求头的网站， 下载保存请求头
# 最后转储redis 方便程序调用
import json
import requests

file = open('./fake_ua.py', 'w+', encoding='utf-8')
file.write('ua = [\n')
tx = requests.get('https://fake-useragent.herokuapp.com/browsers/0.1.11').text
all_ua = json.loads(tx)
# print(all_ua)
# print(type(all_ua))
# print(all_ua['browsers']['chrome'])
# print('-----------------------------------')
for b in all_ua['browsers']:
    for ua in all_ua['browsers'][b]:
        print(ua)
        file.write('\"' + ua + '\"' + ',\n')
# for r in all_ua['randomize']:
#     print(r)
file.write(']')
file.close()
