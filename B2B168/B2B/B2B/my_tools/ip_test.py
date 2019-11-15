import re
import json
import telnetlib
# import random
import redis
import requests


class IPTest(object):

    def __init__(self):
        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)
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
    def put_to_redis(self, ip_host, ip_port):
        proxy_url = 'http://' + ip_host + ':' + ip_port
        self.connect.lpush(self.proxy_key, proxy_url)
        print('this IP is saving to redis!!!')

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
            self.connect.lrem(self.proxy_key, 0, ip_url)
        print('This ip is useful!!!')

    # 如果IP被封或者定向302出验证码等情况, 需要删除代理IP并且把网页加入到失败的请求队列中
    def del_ip(self, ip_url):
        if ip_url in [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in range(self.connect.llen(self.proxy_key))]:
            self.connect.lrem(self.proxy_key, 0, ip_url)

    def get_ip(self):
        # '39.107.59.59'
        # api_url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=7a8a979e9247421688fdc7eebf380cd2&count=20&expiryDate=0&format=2&newLine=3'
        # all_proxy = requests.get(api_url).text
        # print(all_proxy)
        # all_proxy = re.compile(r'(.*?):(\d+)').findall(all_proxy)
        text = requests.get('http://39.107.59.59/get').text
        json_text = json.loads(text)
        ip_ls = json_text['RESULT']
        ips = []
        for ip in ip_ls:
            host = ip['ip']
            port = ip['port']
            ips.append(host + ':' + str(port))

        for pro in ips:
            p = pro.split(':')
            pass
            if self.test_ip(p[0], p[1]):
                self.put_to_redis(p[0], p[1])
                pass
            else:
                pass


IPTest().get_ip()
