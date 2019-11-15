# import re
from urllib.parse import unquote
# ls = ['', '', 1, 5, 8]
#
# cat = ls[0] if ls[0] else 'null'
# print(cat)
# hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=column&q=%E5%B0%8F%E7%B1%B3&correction=1&offset=0&' \
#            'limit=10&show_all_topics=0&search_hash_id=6177de39e96dbfaefebfacd5c70732a0'
#
# for i in range(5):
#     page = int((int(re.compile('offset=(.*?)&limit=10').findall(hash_url)[0]) - 5) / 10)
#     print(page + 1)
#     hash_url = hash_url.replace(str(page), '%s' % str(5 + (page + 1) * 10))
#     print(hash_url)
print(unquote('%E5%B0%8F%E7%B1%B3'))
