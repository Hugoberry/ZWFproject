import redis

coon = redis.Redis(host='localhost', port=6379, db=0)
for i in range(10):
    x = coon.lpop('A')
    print(x)
