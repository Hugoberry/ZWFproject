from scrapy_redis.spiders import RedisSpider
import re
from xpinyin import Pinyin
from scrapy.spidermiddlewares.httperror import HttpError, logger
from twisted.internet.error import *
import scrapy
from DomainRedis.items import DomaintestItem
import redis
from main import num
# num = '6'

keyword_key = 'keyword_key%s' % num


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'com_demo_%s' % num
    redis_key = 'com_domain:start_urls'
    allowed_domains = ['net.cn']
    start_urls = ['http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=quandashi.com']

    def __init__(self):
        super(MySpider).__init__()

        self.connect = redis.Redis(host='10.0.1.87', port=6379, db=15)

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            pass
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.response
            logger.error('HttpError on %s', response.url)

    def parse(self, response):
        while True:
            kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
            print(kw)
            item = DomaintestItem()
            item['kw'] = kw
            kw_pinyin = Pinyin().get_pinyin(kw).replace('-', '').replace(' ', '').replace('.', '').replace('·', '')\
                .replace(' ', '').replace(';', '').lower()
            domain_type_ls = ['com']
            for domain_tp in domain_type_ls:
                aim_url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=' + kw_pinyin + '.' + domain_tp
                yield scrapy.Request(url=aim_url, callback=self.parse_detail, meta={'item': item},
                                     errback=self.errback_twisted)

    def parse_detail(self, response):
        item = response.meta['item']
        item['domain_url'] = re.compile('area_domain=(.*)').findall(response.url)[0]
        item['domain_type'] = re.compile(r'.*?\.(.*)').findall(item['domain_url'])[0]
        item['domain_status'] = re.compile('<original>(.*)</original>').findall(response.text)[0]
        yield item
