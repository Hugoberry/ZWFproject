import redis

keyword_key = 'keyword_key'
connect = redis.Redis(host='127.0.0.1', port=6379, db=2)
# proxy_key = 'proxy_key'
# ip_ls = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
# print(len(ip_ls))
# for i in ip_ls:
#     print(i)

for x in range(10):
    kw = connect.lindex(keyword_key, x).decode('utf-8').strip()
    connect.lrem(keyword_key, kw)
    print(kw)
