import re
import redis

connect = redis.Redis(host='10.10.22.113', port=6379, db=5)
for k in range(4):
    file = open('./kw/%s.txt' % str(k + 1), 'r+', encoding='utf-8')
    line = file.readlines()
    for i in line:
        try:
            result = re.compile('(.*?)\d+').findall(i)[0].strip()
            print(result)
            connect.lpush("company_queue", result)
        except IndexError:
            pass
