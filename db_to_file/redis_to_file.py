import redis
import json

# connect = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


def save_to_file(file_name, file_type):
    file = open('%s.%s' % (file_name, file_type), 'w+', encoding='utf-8')
    return file


def connect_to_redis(redis_host, redis_port, redis_db):
    connect = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    return connect


def get_all_value(redis_host, redis_port, redis_db, redis_key, file_name, file_type):
    connect = connect_to_redis(redis_host, redis_port, redis_db)
    list_len = connect.llen(redis_key)
    file = save_to_file(file_name, file_type)
    for item in range(list_len):
        word = connect.lindex(redis_key, item)
        word = json.loads(word.decode('utf-8'))
        file.write(json.dumps(word, ensure_ascii=False) + '\n')
        print(word)
    file.close()
    print('finished!!!')

# l_len = connect.llen('')
# len_c = connect.lindex('zh_live_redis:items', 0)
# print(type(len_c))
# # print(len_c.decode('utf-8'))
# d = json.loads(len_c.decode('utf-8'))
# print(d)
# print(type(d))


get_all_value('127.0.0.1', 6379, 15, 'zh_topic_redis:items', 'zh_topic_json', 'txt')
