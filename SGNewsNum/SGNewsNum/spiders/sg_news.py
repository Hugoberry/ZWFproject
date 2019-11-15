import re
from urllib.parse import quote
from scrapy.spidermiddlewares.httperror import HttpError, logger
from twisted.internet.error import *
import scrapy
from scrapy_redis.spiders import RedisSpider
from SGNewsNum.items import SearchItem
import redis
# from my_tools.gen_kw import get_key

connect = redis.Redis(host='127.0.0.1', port=6379, db=11)
keyword_key = 'keyword_key'
fail_url = 'fail_url'


class SgSearchSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'sg_news'
    redis_key = 'sg_news:start_urls'
    allowed_domains = ['sogou.com']
    start_urls = ['https://news.sogou.com/']

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            connect.sadd(fail_url, request.url)
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.response
            request = failure.request
            connect.sadd(fail_url, request.url)
            logger.error('HttpError on %s', response.url)

    def parse(self, response):
        # nums = 100
        # for n in range(int(connect.llen(keyword_key) / nums) + 1):
        #     kw_ls = next(get_key(nums))
        #     for kw in kw_ls:
        #         print(kw)
        #         item = SearchItem()
        #         item['kw'] = kw
        #         search_url = response.url + 'news?query=%s' % quote(kw)
        #         print(search_url)
        #         yield scrapy.Request(url=search_url, callback=self.parse_search, meta={'item': item},
        #                              errback=self.errback_twisted)

        for x in range(connect.llen(keyword_key)):
            kw = connect.lindex(keyword_key, 0).decode('utf-8').strip()
            connect.lrem(keyword_key, kw)
            print(kw)
            item = SearchItem()
            item['kw'] = kw
            search_url = response.url + 'news?query=%s' % quote(kw)
            print(search_url)
            yield scrapy.Request(url=search_url, callback=self.parse_search, meta={'item': item},
                                 errback=self.errback_twisted)

    def parse_search(self, response):
        item = response.meta['item']
        news_nums = response.xpath('//div[@class="header-filt"]/span[@class="filt-result"]/text()').extract_first()
        news = re.compile('找到相关新闻约(.*?)篇').findall(news_nums)[0]
        item['news_nums'] = news
        yield item
