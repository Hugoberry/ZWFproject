import redis

keyword_key = 'keyword_key'
connect = redis.Redis(host='10.10.22.113', port=6379, db=15)


def kw_to_redis(file_path):
    # ../a.txt
    file = open(r'%s' % file_path, 'r+', encoding='utf-8')
    line = file.readlines()
    len_len = len(line)
    for word in range(len_len):
        # kw = line[word].replace('(', '').replace(',1)', '').strip()
        kw = line[word].strip()
        connect.lpush(keyword_key, kw)


kw_to_redis('../applicant.txt')


for i in range(connect.llen(keyword_key)):
    print(connect.lindex(keyword_key, i).decode('utf-8'))
