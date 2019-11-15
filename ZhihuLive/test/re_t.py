import re

url = 'https://www.zhihu.com/api/v4/search_v3?t=live&q=%E8%8B%B1%E9%9B%84%E8%81%94%E7%9B%9F&correction=1' \
      '&offset=5&limit=10&show_all_topics=0&search_hash_id=356982194b5b773720d0f0f152775e2d'
(offset, hash_id) = re.compile(r'&offset=(\d+)&limit=10&show_all_topics=0&search_hash_id=(.*)').findall(url)[0]
print(offset)
print(hash_id)
