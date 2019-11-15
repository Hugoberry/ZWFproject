# -*- coding: utf-8 -*-
import redis

import scrapy
import json

from scrapy.spidermiddlewares.httperror import HttpError, logger
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TCPTimedOutError, DNSLookupError

from EUIPO_REDIS.items import RelationItem
from main import num
from my_tools.pt_demo import IPCookie

empty_word = 'null'
keyword_key = 'keyword_key'
ip_cookie_key = 'ip_cookie_key_%s' % num


class IpoRelationSpider(RedisSpider):
    name = 'ipo_relation'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['https://www.baidu.com/']
    redis_key = 'ipo_relation:start_urls'

    def __init__(self):
        super(IpoRelationSpider).__init__()
        self.connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
        try:
            self.cookie = json.loads(list(eval(self.connect.lindex(ip_cookie_key, 0).decode('utf-8')))[1])
        except Exception as e:
            print(e)
            IPCookie().get_cookies()
            self.cookie = json.loads(list(eval(self.connect.lindex(ip_cookie_key, 0).decode('utf-8')))[1])

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            while True:
                self.connect.blpop(ip_cookie_key, 1)
                if self.connect.llen(ip_cookie_key) == 0:
                    break
            IPCookie().get_cookies()

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            while True:
                self.connect.blpop(ip_cookie_key, 1)
                if self.connect.llen(ip_cookie_key) == 0:
                    break
            IPCookie().get_cookies()

            response = failure.response
            logger.error('HttpError on %s', response.url)

    def parse(self, response):

        try:

            while True:
                nums = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                print(nums)
                first_url = 'https://euipo.europa.eu/copla//trademark/data/withOppoRelations/%s' % nums

                yield scrapy.Request(url=first_url, callback=self.parse_relation, cookies=self.cookie, meta={'nums': nums}, errback=self.errback_twisted)

        except TypeError:
            pass

    def parse_relation(self, response):

        nums = response.meta['nums']
        print(nums)
        json_text = json.loads(response.text, encoding='utf-8')

        item = RelationItem()

        item['nums'] = nums
        item['commonDescriptor'] = str(json_text['commonDescriptor'])
        item['entity'] = str(json_text['entity'])
        item['oppoPermissions'] = str(json_text['oppoPermissions'])
        item['permissions'] = str(json_text['permissions'])
        item['relations'] = str(json_text['relations'])

        yield item
