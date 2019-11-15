import random
from urllib.parse import *
from my_tools.ip_test import *
from SGNews_req.fake_ua import ua

keyword_key = 'keyword_key'
time_ls = [3.6, 5.2, 5.1, 4.2, 2.9, 5.22, 6.01, 4.88, 4.95, 3.86, 3.82, 3.55, 5.09]
connect = redis.Redis(host='127.0.0.1', port=6379, db=7)


def get_key(nums):
    all_kw = []
    for x in range(nums):
        kw = connect.lindex(keyword_key, 0).decode('utf-8').strip()
        connect.lrem(keyword_key, kw)
        all_kw.append(kw)
    yield all_kw


def get_all_news(kw_ls):
    file = open('./sg_news.txt', 'a+', encoding='utf-8')
    for kw in kw_ls:
        search_url = 'https://news.sogou.com/news?query=%s' % quote(kw)
        headers = {
            'User-Agent': random.choice(ua),
            'Referer': 'https://news.sogou.com/',
        }
        ip_ls = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
        if len(ip_ls) < 3:
            get_ip()
        ip = random.choice(ip_ls)
        ip = re.compile('http://(.*)').findall(ip)[0]
        proxies = {
            'http': ip,
        }
        try:
            text = requests.get(url=search_url, headers=headers, allow_redirects=False, proxies=proxies)
            print(text.headers)
            print(text.url)
            par = re.compile('<span class="filt-result">找到相关新闻约(.*)篇</span>').findall(text.text)[0]
            print(kw, par)
            # time.sleep(random.choice(time_ls))
            if par:
                connect.lpush('success_kw', kw)
            file.write(kw + 'ÿ' + par + '\n')
            file.flush()
        except IndexError:
            print('fail == ', kw)
            connect.lrem(proxy_key, 'http://' + ip)
            connect.sadd('fail_key', kw)
            # time.sleep(random.choice(time_ls))

    file.close()


aim_nums = 80
for n in range(int(connect.llen(keyword_key) / aim_nums) + 1):
    keyword_ls = next(get_key(aim_nums))
    get_all_news(keyword_ls)
