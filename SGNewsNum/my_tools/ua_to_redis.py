# 这是从获得的UA 里取到所有的UA 并且保存到redis， 以我本地的redis为例
from .fake_ua import ua
import random
import redis

connect = redis.Redis(host='10.10.22.113', port=6379, db=2)
for i in range(len(ua)):
    connect.set(i, ua[i])
print(random.choice(ua))
print(connect.get(str(random.randint(0, 250))).decode('utf-8'))
