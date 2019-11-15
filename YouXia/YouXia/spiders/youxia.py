# -*- coding: utf-8 -*-
import redis
import scrapy
from urllib.parse import *

from scrapy_redis.spiders import RedisSpider

from YouXia.items import YouxiaItem
from main import num

empty_word = 'null'
keyword_key = 'keyword_key_%s' % num


class YouxiaSpider(RedisSpider):
    name = 'youxia_%s' % num
    allowed_domains = ['ali213.net']
    redis_key = 'youxia:start_urls'
    start_urls = ['http://ali213.net/']

    def __init__(self):
        super(YouxiaSpider).__init__()

        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

    def parse(self, response):
        while True:
            try:
                kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()

                url = 'http://so.ali213.net/s/s?sub=91&page=1&keyword=%s' % quote(kw)
                yield scrapy.Request(url=url, callback=self.parse_first_page, meta={'kw': kw})
            except TypeError:
                break

    def parse_first_page(self, response):
        kw = response.meta['kw']
        all_pages = response.xpath('//div[@class="contentHeader"]/ul[@class="firstLevelContent"]/li[@class="toggle'
                                   'Content checked"]/ul[@class="secondLevel clearFloat"]/li[@class="toggleBtn chec'
                                   'ked"]/a/span/text()').extract_first()
        if all_pages == '0':
            item = YouxiaItem()
            item['game_kw'] = kw
            item['game_name'] = empty_word
            item['game_type'] = empty_word
            item['game_url'] = empty_word
            item['game_img_url'] = empty_word
            yield item
        else:
            pages = int(int(all_pages) / 30) + 1
            con = response.xpath('//div[@class="resultContent"]/div[@class="glModual1"]/div/a')
            for info in con:
                item = YouxiaItem()
                item['game_kw'] = kw
                item['game_name'] = info.xpath('./img/@alt').extract_first()
                item['game_type'] = info.xpath('./span/text()').extract_first()
                item['game_url'] = info.xpath('./@href').extract_first()
                item['game_img_url'] = info.xpath('./img/@src').extract_first()
                yield item

            if pages >= 2:
                for i in range(2, pages + 1):
                    url = 'http://so.ali213.net/s/s?sub=91&page=%s&keyword=%s' % (str(i), quote(kw))

                    yield scrapy.Request(url=url, callback=self.parse_other_page, meta={'kw': kw})

    def parse_other_page(self, response):
        kw = response.meta['kw']
        con = response.xpath('//div[@class="resultContent"]/div[@class="glModual1"]/div/a')
        for info in con:
            item = YouxiaItem()
            item['game_kw'] = kw
            item['game_name'] = info.xpath('./img/@alt').extract_first()
            item['game_type'] = info.xpath('./span/text()').extract_first()
            item['game_url'] = info.xpath('./@href').extract_first()
            item['game_img_url'] = info.xpath('./img/@src').extract_first()
            yield item
