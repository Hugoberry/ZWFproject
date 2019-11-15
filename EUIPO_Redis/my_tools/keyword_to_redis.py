import redis


class KWRedis:

    def __init__(self):
        self.keyword_key = 'keyword_key'
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


KWRedis().kw_to_redis('./test_img.txt')

print('finished!!!')
