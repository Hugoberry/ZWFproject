import redis

connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
kw = connect.blpop('keyword_key6', timeout=60)[1].decode('utf-8')
print(kw)
pass
