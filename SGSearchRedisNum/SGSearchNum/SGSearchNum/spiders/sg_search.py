import re
from urllib.parse import quote
from scrapy.spidermiddlewares.httperror import HttpError, logger
from twisted.internet.error import *
import scrapy
from scrapy_redis.spiders import RedisSpider
from SGSearchNum.items import SearchItem
import redis

connect = redis.Redis(host='127.0.0.1', port=6379, db=2)
keyword_key = 'keyword_key'
fail_url = 'fail_url'


class SgSearchSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'sg_search'
    redis_key = 'sg_search:start_urls'
    allowed_domains = ['sogou.com']
    start_urls = ['https://www.sogou.com/']

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            connect.sadd(fail_url, request.url)
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            request = failure.value.request
            connect.sadd(fail_url, request.url)
            logger.error('HttpError on %s', response.url)

    def parse(self, response):
        for x in range(connect.llen(keyword_key)):
            kw = connect.lindex(keyword_key, 0).decode('utf-8').strip()
            connect.lrem(keyword_key, kw)
            print(kw)
            item = SearchItem()
            item['kw'] = kw
            search_url = response.url + 'web?query=%s' % quote(kw)
            print(search_url)
            yield scrapy.Request(url=search_url, callback=self.parse_search, meta={'item': item}, errback=self.errback_twisted)

    def parse_search(self, response):
        item = response.meta['item']
        search_nums = response.xpath('//div[@class="search-info"]/p[@class="num-tips"]/text()').extract_first()
        nums = re.compile(r'搜狗已为您找到约(.*?)条相关结果').findall(search_nums)[0]
        item['search_nums'] = nums
        yield item
