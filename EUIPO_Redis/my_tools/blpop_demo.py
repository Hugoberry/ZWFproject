import redis

connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
while True:
    connect.blpop('a', 1)
    if connect.llen('a') == 0:
        break
