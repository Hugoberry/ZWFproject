import random
import re
from urllib.parse import quote
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from Search360Redis.items import Search360Item
# import redis
from twisted.internet.error import *
from my_tools.ip_test import *

fail_url = 'fail_url'
keyword_key = 'keyword_key'
proxy_key = 'proxy_key'
empty_word = '0'
connect = redis.Redis(host='127.0.0.1', port=6379, db=15)


class Sear360Spider(scrapy.Spider):
    name = 'sear_360'
    redis_key = 'search360:start_urls'
    allowed_domains = ['so.com']
    start_urls = ['https://www.so.com/']

    # twisted 异步请求异常捕获函数
    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            connect.rpush(fail_url, request.url)
        elif failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            request = failure.request
            # company_name = request.meta["company_name"]
            connect.sadd(fail_url, request.url)
        elif failure.check(TypeError):
            request = failure.request
            ip_ls = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
            print(len(ip_ls))
            if len(ip_ls) < 3:
                get_ip()
            ip = random.choice(ip_ls)
            [proxy_host, proxy_port] = re.compile(r'http://(.*?):(\d+)').findall(ip)[0]
            if not test_ip(proxy_host, proxy_port):
                del_ip('http://' + proxy_host + ':' + proxy_port)
            else:
                request.meta['proxy'] = ip

    def parse(self, response):
        for x in range(connect.llen(keyword_key)):
            kw = connect.lindex(keyword_key, 0).decode('utf-8').strip()
            connect.lrem(keyword_key, kw)
            print(kw)
            item = Search360Item()
            item['kw'] = kw
            search_url = response.url + 's?ie=utf-8&fr=none&src=360sou_newhome&q=%s' % quote(kw)
            yield scrapy.Request(url=search_url, callback=self.parse_search, meta={'item': item}, errback=self.errback_twisted)

    def parse_search(self, response):
        item = response.meta['item']
        null_str = response.xpath("//div[@id='container']/div[@id='no-result']/p[@class='tips']").extract_first()
        if null_str:
            item['search_nums'] = empty_word
            yield item
        search_nums_str = response.xpath('//div[@id="page"]/span[@class="nums"]/text()').extract_first()
        if search_nums_str:
            search_nums = re.compile('找到相关结果约(.*?)个').findall(search_nums_str)[0]
            print(search_nums)
            item['search_nums'] = search_nums
            yield item
