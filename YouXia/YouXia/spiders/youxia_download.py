# -*- coding: utf-8 -*-
import redis
import scrapy
from urllib.parse import *
import re

from scrapy_redis.spiders import RedisSpider

from YouXia.items import YouxiaDownloadItem

empty_word = 'null'
keyword_key = 'keyword_key'


class YouxiaSpider(RedisSpider):
    name = 'youxia_download'
    allowed_domains = ['ali213.net']
    redis_key = 'youxia:start_urls'
    start_urls = ['http://ali213.net/']

    def __init__(self):
        super(YouxiaSpider).__init__()

        self.redis_connect_pool = redis.ConnectionPool(host='localhost', port=6379, db=15)
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

    def parse(self, response):
        while True:
            try:
                kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()

                url = 'http://so.ali213.net/s/s?sub=93&page=1&keyword=%s' % quote(kw)
                yield scrapy.Request(url=url, callback=self.parse_first_page, meta={'kw': kw})
            except TypeError:
                break

    def parse_first_page(self, response):
        kw = response.meta['kw']
        all_pages = response.xpath('//div[@class="contentHeader"]/ul[@class="firstLevelContent"]/li[@class="toggle'
                                   'Content checked"]/ul[@class="secondLevel clearFloat"]/li[@class="toggleBtn chec'
                                   'ked"]/a/span/text()').extract_first()
        if all_pages == '0':
            item = YouxiaDownloadItem()
            item['game_kw'] = kw
            item['download_title'] = empty_word
            item['download_url'] = empty_word
            item['file_size'] = empty_word
            item['publish_time'] = empty_word
            item['describe'] = empty_word
            yield item
        else:
            pages = int(int(all_pages) / 10) + 1
            con = response.xpath(
                '//div[@class="resultContent"]/div[@class="sameModual downLoadModual"]/ul[@class="glList"]/li')
            for info in con:
                item = YouxiaDownloadItem()
                item['game_kw'] = kw
                # <font class="highlight"><font class="highlight">英雄</font><font class="highlight">联<font class="highlight">盟</font></font></font>
                download_title_re = info.xpath('./a').extract_first().replace('<font class="highlight">', '').replace(
                    '</font>', '').replace('"', '')
                download_title = re.compile(r'class=glTitle>(.*)</a>').findall(download_title_re)
                if download_title:
                    item['download_title'] = download_title[0]
                else:
                    item['download_title'] = download_title_re
                item['download_url'] = info.xpath('./a/@href').extract_first()
                item['file_size'] = info.xpath('./p[1]/em/text()').extract_first()
                item['publish_time'] = info.xpath('./span/text()').extract_first()
                item['describe'] = info.xpath('./p[2]').extract_first().replace('<font class="highlight">', '').replace(
                    '</font>', '').replace('"', '').replace('\r\n', '')
                yield item

            if pages >= 2:
                if pages >= 100:
                    for i in range(2, 101):
                        url = 'http://so.ali213.net/s/s?sub=93&page=%s&keyword=%s' % (str(i), quote(kw))

                        yield scrapy.Request(url=url, callback=self.parse_other_page, meta={'kw': kw})
                else:
                    for i in range(2, pages + 1):
                        url = 'http://so.ali213.net/s/s?sub=93&page=%s&keyword=%s' % (str(i), quote(kw))

                        yield scrapy.Request(url=url, callback=self.parse_other_page, meta={'kw': kw})

    def parse_other_page(self, response):
        kw = response.meta['kw']
        con = response.xpath(
            '//div[@class="resultContent"]/div[@class="sameModual downLoadModual"]/ul[@class="glList"]/li')
        for info in con:
            item = YouxiaDownloadItem()
            item['game_kw'] = kw
            download_title_re = info.xpath('./a').extract_first().replace('<font class="highlight">', '').replace(
                '</font>', '').replace('"', '')
            download_title = re.compile(r'class=glTitle>(.*)</a>').findall(download_title_re)
            if download_title:
                item['download_title'] = download_title[0]
            else:
                item['download_title'] = download_title_re
            item['download_url'] = info.xpath('./a/@href').extract_first()
            item['file_size'] = info.xpath('./p[1]/em/text()').extract_first()
            item['publish_time'] = info.xpath('./span/text()').extract_first()
            item['describe'] = info.xpath('./p[2]').extract_first().replace('<font class="highlight">', '').replace(
                '</font>', '').replace('"', '').replace('\r\n', '')
            yield item
