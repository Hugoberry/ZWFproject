import redis
import sys

num = sys.argv[1]
# num = 0


class KWRedis:

    def __init__(self):
        self.keyword_key = 'keyword_key%s' % str(num)
        self.connect = redis.Redis(host='127.0.0.1', port=6379, db=15)

    def kw_to_redis(self, file_path):
        # ../a.txt
        file = open(r'%s' % file_path, 'r+', encoding='utf-8')
        while True:
            lines = file.readlines(16384)
            if not lines:
                break
            for line in lines:
                kw = line.replace('\n', '').strip()
                self.connect.lpush(self.keyword_key, kw)
        file.close()


KWRedis().kw_to_redis('./kw_file/tm_%s.txt' % str(num))

print('finished!!!')
