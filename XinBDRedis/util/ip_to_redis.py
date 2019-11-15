import redis
from util.db import get_redis_cli
from util.proxies import Proxies
import time

connect = redis.Redis(host='10.10.22.113', port=6379, db=3)
for i in range(30):
    ip = Proxies(get_redis_cli()).get_proxies(update=True)
    ip = 'http://' + ip['ip'] + ':' + ip['port']
    print(ip)
    connect.set(str(i), ip)
    time.sleep(2)
