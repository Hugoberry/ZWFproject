import re
import telnetlib
# import random
import redis
import requests

connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
proxy_key = 'proxy_key'


def test_ip(ip_host, ip_port, timeout=2):
    try:
        telnetlib.Telnet(host=ip_host, port=ip_port, timeout=timeout)
    except Exception as e:
        print(e)
        # proxy_name = 'http://' + ip_host + ':' + ip_port
        # connect.lrem(proxy_key, proxy_name)
        return False
    else:
        return True


# 将测试好的ip存入redis数据库
def put_to_redis(ip_host, ip_port, timeout=2):
    if test_ip(ip_host, ip_port, timeout):
        proxy_url = 'http://' + ip_host + ':' + ip_port
        if proxy_url in [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]:
            print('this IP is existed in ip list!!!')
        else:
            connect.lpush(proxy_key, proxy_url)
            print('this IP is saving to redis!!!')
    else:
        print('this ip was wrong!!!')


# 检测将无效的IP移除数据库
# def del_to_redis(all_proxy=[connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]):
#     # all_proxy = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
#     print(all_proxy)
#     for p in all_proxy:
#         [proxy_host, proxy_port] = re.compile(r'http://(.*?):(\d+)').findall(p)[0]
#         if not test_ip(proxy_host, proxy_port):
#             connect.lrem(proxy_key, p)


# 检测将无效的IP移除数据库
def del_to_redis(ip_url):
    [proxy_host, proxy_port] = re.compile(r'http://(.*?):(\d+)').findall(ip_url)[0]
    if not test_ip(proxy_host, proxy_port):
        connect.lrem(proxy_key, 0, ip_url)
    print('This ip is useful!!!')


# 如果IP被封或者定向302出验证码等情况, 需要删除代理IP并且把网页加入到失败的请求队列中
def del_ip(ip_url):
    if ip_url in [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]:
        connect.lrem(proxy_key, 0, ip_url)


def get_ip():
    # '39.107.59.59'
    # api_url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=7a8a979e9247421688fdc7eebf380cd2&count=20&expiryDate=0&format=2&newLine=3'
    # all_proxy = requests.get(api_url).text
    # print(all_proxy)
    # all_proxy = re.compile(r'(.*?):(\d+)').findall(all_proxy)
    text = requests.get('http://39.107.59.59/get').text.replace('\\', '').split('["')[1].split('"]')[0]
    ip_ls = text.split('",')
    ips = []
    for ip in ip_ls:
        ip_dict = eval(ip.replace('"{', '{'))
        ips.append((ip_dict['ip'], str(ip_dict['port'])))

    for pro in ips:
        if test_ip(pro[0], pro[1]):
            put_to_redis(pro[0], pro[1])
        else:
            pass


get_ip()
ip_ls = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
print(len(ip_ls))
