import re
from urllib.parse import quote
import scrapy
import redis

from scrapy_redis.spiders import RedisSpider
from BDSearchRedis.items import SearchItem
from main import num

keyword_key = 'keyword_key%s' % num


class BaiduSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'bd_search_%s' % num
    redis_key = 'bd_search:start_urls'
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/']

    def __init__(self):
        super(BaiduSpider).__init__()

        self.connect = redis.Redis(host='127.0.0.1', port=6379, db=15)

    def parse(self, response):
        while True:
            kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
            print(kw)
            item = SearchItem()
            item['kw'] = kw
            url = response.url + 's?wd=%s' % quote(kw)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        nums_str = response.xpath('//div[@class="nums"]/span/text()').extract_first()
        print(nums_str)
        nums = re.compile(r'百度为您找到相关结果约(.*)个').findall(nums_str)[0]
        item['search_nums'] = nums
        print(response.url)
        # 'https://www.baidu.com/s?tn=news&word=%E8%99%BE%E7%B1%B3'
        print(nums)
        news_url = 'http://news.baidu.com/ns?word=%s&tn=news&from=news&cl=2&rn=20&ct=1' % quote(item['kw'])
        print(news_url)
        yield scrapy.Request(url=news_url, callback=self.parse_news, meta={'item': item})

    def parse_news(self, response):
        item = response.meta['item']
        news_str = response.xpath('//div[@id="header_top_bar"]/span/text()').extract_first()
        news_nums = re.compile(r'找到相关新闻(.*)篇').findall(news_str)
        if news_nums:
            if '约' in news_nums[0]:
                item['news_nums'] = news_nums[0].split('约')[1]
            else:
                item['news_nums'] = news_nums[0]
            yield item
        else:
            item['news_nums'] = '0'
            yield item
