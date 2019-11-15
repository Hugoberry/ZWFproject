# -*- coding: utf-8 -*-
import time
import redis

import scrapy
import json

from scrapy.spidermiddlewares.httperror import HttpError, logger
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TCPTimedOutError, DNSLookupError

from main import num
from my_tools.pt_demo import IPCookie
from EUIPO_REDIS.items import TimelineItem
# from my_tools.pt_demo import get_cookies

empty_word = 'null'
keyword_key = 'keyword_key'
ip_cookie_key = 'ip_cookie_key_%s' % num


class IpoSpider(RedisSpider):
    name = 'ipo_timeline'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['https://www.baidu.com/']
    redis_key = 'ipo:start_urls'

    def __init__(self):
        super(IpoSpider).__init__()
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
                first_url = 'https://euipo.europa.eu/copla/timeline/trademark/%s' % nums

                yield scrapy.Request(url=first_url, callback=self.parse_timeline, cookies=self.cookie, meta={'nums': nums}, errback=self.errback_twisted)

        except TypeError:
            pass

    def parse_timeline(self, response):

        nums = response.meta['nums']
        print(nums)
        json_text = json.loads(response.text, encoding='utf-8')

        item = TimelineItem()

        item['nums'] = nums
        item['actualDate'] = str(json_text['actualDate'])
        item['actualDateLabel'] = str(json_text['actualDateLabel'])
        item['actualStatusLabel'] = str(json_text['actualStatusLabel'])
        item['milestones'] = str(json_text['milestones'])
        item['totalSteps'] = str(json_text['totalSteps'])

        yield item

        time.sleep(10)
