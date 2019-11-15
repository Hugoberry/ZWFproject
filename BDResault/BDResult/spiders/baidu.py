# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
import re

from scrapy_redis.spiders import RedisSpider

from BDResult.items import SearchItem
from main import num
import redis

empty_word = 'null'
keyword_key = 'keyword_key_%s' % num


class BaiduSpider(RedisSpider):
    name = 'baidu_%s' % num
    redis_key = 'baidu:start_urls'
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/']

    def __init__(self):
        super(BaiduSpider).__init__()

        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

    def parse(self, response):
        while True:
            try:
                kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                url = response.url + 's?wd=%s' % quote(kw.strip())
                yield scrapy.Request(url=url, callback=self.parse_detail, meta={'kw': kw})
            except TypeError:
                break

    def parse_detail(self, response):
        kw = response.meta['kw']
        nums_str = response.xpath('//div[@class="nums"]/span/text()').extract_first()
        nums = re.compile(r'百度为您找到相关结果约(.*?)个').findall(nums_str)[0].replace(',', '')
        titles = response.xpath('//div[@id="content_left"]/div/h3/a[1]')
        for title in titles:
            item = SearchItem()
            item['kw'] = kw
            a = title.extract()
            res = re.compile(r'target="_blank">(.*)</a>').findall(a)
            if res:
                result = res[0].replace('<em>', '').replace('</em>', '')
                link_url = title.xpath('./@href').extract_first()
                item['search_nums'] = nums
                item['title'] = result
                item['link_url'] = link_url
                yield item
            else:
                result = empty_word
                link_url = title.xpath('./@href').extract_first()
                item['search_nums'] = nums
                item['title'] = result
                item['link_url'] = link_url
                yield item
        # 'https://www.baidu.com/s?tn=news&word=%E8%99%BE%E7%B1%B3'
        if int(nums) > 40:
            for x in range(4):
                news_url = 'https://www.baidu.com/s?wd=%s&pn=10&oq=%s&ie=utf-8&usm=%s' % (
                    quote(kw), quote(kw), str(x + 2))
                yield scrapy.Request(url=news_url, callback=self.parse_other, meta={'kw': kw, 'nums': nums})
        else:
            for x in range(int(nums / 10)):
                news_url = 'https://www.baidu.com/s?wd=%s&pn=10&oq=%s&ie=utf-8&usm=%s' % (
                    quote(kw), quote(kw), str(x + 2))
                yield scrapy.Request(url=news_url, callback=self.parse_other, meta={'kw': kw, 'nums': nums})

    def parse_other(self, response):
        kw = response.meta['kw']
        nums = response.meta['nums']
        titles = response.xpath('//div[@id="content_left"]/div/h3/a[1]')
        for title in titles:
            item = SearchItem()
            a = title.extract()
            res = re.compile(r'target="_blank">(.*)</a>').findall(a)
            if res:
                result = res[0].replace('<em>', '').replace('</em>', '')
                link_url = title.xpath('./@href').extract_first()
                item['kw'] = kw
                item['search_nums'] = nums
                item['title'] = result
                item['link_url'] = link_url
                yield item
            else:
                result = empty_word
                link_url = title.xpath('./@href').extract_first()
                item['kw'] = kw
                item['search_nums'] = nums
                item['title'] = result
                item['link_url'] = link_url
                yield item
