import re

s = 'http://www.zhihu.com/search_v3?content_length=150&vertical_info=0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0&' \
    'advert_count=0&correction=1&search_hash_id=5453e33e2bee1057276ad68ad752e11c&q=%E4%B8%AD%E5%9B%BD&limit' \
    '=10&t=live&offset=25&topic_filter=0'

new_url = re.compile(r'&search_hash_id=(.*?)&q=(.*?)&limit=10&t=live&offset=(\d+)&topic_filter=0').findall(s)[0]
print(new_url)
