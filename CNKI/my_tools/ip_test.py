import re
import telnetlib
# import random
import redis
import requests


class IpTest(object):

    def __init__(self):
        self.pool = redis.ConnectionPool(host='127.0.0.1', port=6379, max_connections=10)
        self.connect = redis.Redis(connection_pool=self.pool, decode_responses=True)
        self.proxy_key = 'proxy_key'

    def test_ip(self, ip_host, ip_port, timeout=2):
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
    def put_to_redis(self, ip_host, ip_port, timeout=2):
        if self.test_ip(ip_host, ip_port, timeout):
            proxy_url = 'http://' + ip_host + ':' + ip_port
            if proxy_url in [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in range(self.connect.llen(self.proxy_key))]:
                print('this IP is existed in ip list!!!')
            else:
                self.connect.lpush(self.proxy_key, proxy_url)
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
    def del_to_redis(self, ip_url):
        [proxy_host, proxy_port] = re.compile(r'http://(.*?):(\d+)').findall(ip_url)[0]
        if not self.test_ip(proxy_host, proxy_port):
            self.connect.lrem(self.proxy_key, ip_url, 0)
        print('This ip is useful!!!')

    # 如果IP被封或者定向302出验证码等情况, 需要删除代理IP并且把网页加入到失败的请求队列中
    def del_ip(self, ip_url):
        # if ip_url in [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in range(self.connect.llen(self.proxy_key))]:
        try:
            self.connect.lrem(self.proxy_key, ip_url, 0)
        except Exception as e:
            print(e)

    def get_ip(self):
        api_url = 'http://d.jghttp.golangapi.com/getip?num=3&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=4&sb=0&pb=4&mr=1&regions='
        all_proxy = requests.get(api_url).text
        print(all_proxy)
        all_proxy = re.compile(r'(.*?):(\d+)').findall(all_proxy)
        for pro in all_proxy:
            print(pro)
            if self.test_ip(pro[0], pro[1]):
                self.put_to_redis(pro[0], pro[1])
            else:
                pass


# get_ip()
# ip_ls = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
# print(len(ip_ls))
