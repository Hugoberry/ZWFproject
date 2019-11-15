# -*- coding: utf-8 -*-
import redis

import scrapy
import json

from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TCPTimedOutError, DNSLookupError

from EUIPO_REDIS.items import CommunicationsItem
from main import num
from my_tools.pt_demo import IPCookie

empty_word = 'null'
keyword_key = 'keyword_key'
ip_cookie_key = 'ip_cookie_key_%s' % num


class IpoSpider(RedisSpider):
    name = 'ipo_communications'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['https://www.baidu.com/']
    redis_key = 'ipo:start_urls'

    def __init__(self):
        super(IpoSpider).__init__()
        # self.redis_connect_pool = redis.ConnectionPool(host='40.73.36.3', port=6667, db=15, password='quandashi2018')
        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)
        try:
            self.cookie = json.loads(list(eval(self.connect.lindex(ip_cookie_key, 0).decode('utf-8')))[1])
        except Exception as e:
            print(e)
            IPCookie().get_cookies()
            self.cookie = json.loads(list(eval(self.connect.lindex(ip_cookie_key, 0).decode('utf-8')))[1])

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            for x in range(2):
                self.connect.blpop(ip_cookie_key, 1)
                if self.connect.llen(ip_cookie_key) == 0:
                    break
            IPCookie().get_cookies()

    def parse(self, response):

        if self.connect.zcard(self.name + ":requests") == 0:
            try:
                for x in range(10000):
                    nums = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                    first_url = 'https://euipo.europa.eu/copla/communications/menu/CTM/%s' % nums
                    yield scrapy.Request(url=first_url, callback=self.parse_communications, cookies=self.cookie,
                                         meta={'nums': nums}, errback=self.errback_twisted)
            except Exception as e:
                print(e)

    def parse_communications(self, response):

        nums = response.meta['nums']
        json_text = json.loads(response.text, encoding='utf-8')
        item = CommunicationsItem()
        item['nums'] = nums
        if response.status == 404:
            item["ctm"] = empty_word
        else:
            item['ctm'] = str(json_text['CTM'])

        yield item
