# -*- coding: utf-8 -*-
import redis

import scrapy
import json
import os

from scrapy.spidermiddlewares.httperror import HttpError, logger
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TCPTimedOutError, DNSLookupError

from main import num
from my_tools.pt_demo import IPCookie

from EUIPO_REDIS.items import ImgItem
# from my_tools.pt_demo import get_cookies

empty_word = 'null'
keyword_key = 'keyword_key'
ip_cookie_key = 'ip_cookie_key_%s' % num


class IpoSpider(RedisSpider):
    name = 'ipo_img'
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
                info = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                [nums, img_url] = info.split('\t')
                print(nums)

                yield scrapy.Request(url=img_url, callback=self.parse_img, cookies=self.cookie, meta={'nums': nums}, errback=self.errback_twisted)

        except TypeError:
            pass

    def parse_img(self, response):
        item = ImgItem()

        nums = response.meta['nums']
        print(nums)
        if not os.path.exists('./EUIPO_IMG/'):
            os.makedirs('./EUIPO_IMG/')

        with open('./EUIPO_IMG/' + nums + '.png', mode='wb+') as fw:
            fw.write(response.body)

        img_path = './EUIPO_IMG/' + nums + '.png'
        img_name = nums + '.png'

        item['nums'] = nums
        item['img_path'] = img_path
        item['img_name'] = img_name
        yield item
