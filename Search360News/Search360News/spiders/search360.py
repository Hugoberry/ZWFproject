import re
import time
from urllib.parse import quote
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from Search360News.items import Search360Item
import redis
from twisted.internet.error import *

fail_url = 'fail_url'
keyword_key = 'keyword_key'
connect = redis.Redis(host='127.0.0.1', port=6379, db=8)


class Sear360Spider(scrapy.Spider):
    name = 'news360'
    redis_key = 'news360:start_urls'
    allowed_domains = ['so.com']
    start_urls = ['https://news.so.com/ns?q=1&src=srp&tn=news']

    # twisted 异步请求异常捕获函数
    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            connect.rpush(fail_url, request.url)
        elif failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            request = failure.value.request
            # company_name = request.meta["company_name"]
            connect.rpush(fail_url, request.url)
        elif failure.check(TypeError):
            time.sleep(10)

    def parse(self, response):
        print('88888888888888888888888')
        for x in range(connect.llen(keyword_key)):
            kw = connect.lindex(keyword_key, 0).decode('utf-8').strip()
            connect.lrem(keyword_key, kw)
            print(kw)
            item = Search360Item()
            item['kw'] = kw
            search_url = 'https://news.so.com/ns?q=%s&src=srp&tn=news' % quote(kw)
            yield scrapy.Request(url=search_url, callback=self.parse_news, meta={'item': item}, errback=self.errback_twisted)

    def parse_news(self, response):
        item = response.meta['item']
        news_nums_str = response.xpath('//div[@class="filter-total"]/text()').extract_first()
        news_nums = re.compile(r'为您推荐相关资讯约(.*?)条').findall(news_nums_str)[0]
        print(news_nums)
        item['news_nums'] = news_nums
        yield item
