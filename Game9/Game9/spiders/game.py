# -*- coding: utf-8 -*-
import redis
import scrapy
from urllib.parse import quote

from Game9.items import Game9Item
from main import num

empty_word = 'null'
keyword_key = 'keyword_key_%s' % num


class GameSpider(scrapy.Spider):
    name = 'game_%s' % num
    allowed_domains = ['9game.cn']
    start_urls = ['http://www.9game.cn/']

    def __init__(self):
        super(GameSpider).__init__()

        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

    def parse(self, response):
        while True:
            try:
                kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                url = 'http://www.9game.cn/search/?keyword={}'.format(quote(kw))
                yield scrapy.Request(url=url, callback=self.parse_first_page, meta={'kw': kw})
            except TypeError:
                break

    def parse_first_page(self, response):

        kw = response.meta['kw']

        all_count = response.xpath('//div[@class="search-amount"]/span/text()').extract_first()
        if not all_count or all_count == '0':
            item = Game9Item()
            item['kw'] = kw
            item['game_name'] = empty_word
            item['game_link'] = empty_word
            item['game_logo'] = empty_word
            item['game_data_type'] = empty_word
            item['game_desc'] = empty_word
            yield item
        else:
            information = response.xpath('//div[@class="sr-poker"]/div[@class="left-con"]')
            for info in information:
                item = Game9Item()

                game_name = info.xpath('./div[@class="sr-img-con"]/a/img/@alt').extract_first()
                game_logo = info.xpath('./div[@class="sr-img-con"]/a/img/@src').extract_first()
                game_link = info.xpath('./div[@class="sr-img-con"]/a/@href').extract_first()
                game_data_type = info.xpath('./div[@class="sr-info-con"]/p[1]/text()').extract_first()
                game_desc = info.xpath('./div[@class="sr-info-con"]/p[2]/text()').extract_first()

                item['kw'] = kw
                item['game_name'] = game_name
                item['game_logo'] = game_logo
                item['game_data_type'] = game_data_type
                item['game_desc'] = game_desc
                item['game_link'] = game_link

                yield item

            if 9 < int(all_count) <= 19:

                ajax_url = 'http://www.9game.cn/tpl/pc2/search/search_result_ajax.html?beginIndex={}&pcount=10&keyword={}'.format('11', quote(kw))
                yield scrapy.Request(url=ajax_url, callback=self.parse_other_page, meta={'kw': kw})

            elif 19 < int(all_count) <= 29:
                for i in range(2):
                    ajax_url = 'http://www.9game.cn/tpl/pc2/search/search_result_ajax.html?beginIndex={}&pcount=10&keyword={}'.format(
                        str(0 * 30 + (i + 1) * 10 + 1), quote(kw))
                    yield scrapy.Request(url=ajax_url, callback=self.parse_other_page, meta={'kw': kw})

            elif int(all_count) > 29:
                pages = int(int(all_count) / 29 + 1)
                if pages >= 5:
                    for x in range(4):
                        new_url = 'http://www.9game.cn/search/?keyword={}&page={}'.format(quote(kw), str(x + 2))
                        yield scrapy.Request(url=new_url, callback=self.parse_other_page, meta={'kw': kw})

                        for i in range(2):
                            ajax_url = 'http://www.9game.cn/tpl/pc2/search/search_result_ajax.html?beginIndex={}&pcount=10&keyword={}'.format(
                                str(x * 30 + (i + 1) * 10 + 1), quote(kw))
                            yield scrapy.Request(url=ajax_url, callback=self.parse_other_page, meta={'kw': kw})
                elif 1 < pages < 5:
                    for x in range(pages - 1):
                        new_url = 'http://www.9game.cn/search/?keyword={}&page={}'.format(quote(kw), str(x + 2))
                        yield scrapy.Request(url=new_url, callback=self.parse_other_page, meta={'kw': kw})
                        for i in range(2):
                            ajax_url = 'http://www.9game.cn/tpl/pc2/search/search_result_ajax.html?beginIndex={}&pcount=10&keyword={}'.format(
                                str(x * 30 + (i + 1) * 10 + 1), quote(kw))
                            yield scrapy.Request(url=ajax_url, callback=self.parse_other_page, meta={'kw': kw})

    def parse_other_page(self, response):

        if str(response.status).startswith == '4' or '5':
            pass
        kw = response.meta['kw']
        information = response.xpath('//div[@class="sr-poker"]/div[@class="left-con"]')
        for info in information:
            item = Game9Item()

            game_name = info.xpath('./div[@class="sr-img-con"]/a/img/@alt').extract_first()
            game_logo = info.xpath('./div[@class="sr-img-con"]/a/img/@src').extract_first()
            game_link = info.xpath('./div[@class="sr-img-con"]/a/@href').extract_first()
            game_data_type = info.xpath('./div[@class="sr-info-con"]/p[1]/text()').extract_first()
            game_desc = info.xpath('./div[@class="sr-info-con"]/p[2]/text()').extract_first()

            item['kw'] = kw
            item['game_name'] = game_name
            item['game_logo'] = game_logo
            item['game_data_type'] = game_data_type
            item['game_desc'] = game_desc
            item['game_link'] = game_link

            yield item
