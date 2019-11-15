# -*- coding: utf-8 -*-
import redis
import scrapy
from urllib.parse import quote
import re

from scrapy_redis.spiders import RedisSpider

from G7k7k.items import G7K7KItem
from main import num

empty_word = 'null'
keyword_key = 'keyword_key_%s' % num


class G7kSpider(RedisSpider):
    name = 'g7k_%s' % num
    allowed_domains = ['7k7k.com']
    redis_key = 'g7k:start_urls'
    start_urls = ['http://7k7k.com/']

    def __init__(self):
        super(G7kSpider).__init__()

        self.redis_connect_pool = redis.ConnectionPool(host='10.0.7.6', port=6667, db=15, password='quandashi2018')
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

    def parse(self, response):
        while True:
            try:
                kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                url = 'http://so.7k7k.com/game/{}.htm'.format(quote(kw))
                yield scrapy.Request(url=url, callback=self.parse_first_page, meta={'kw': kw})
            except TypeError:
                break

    def parse_first_page(self, response):

        kw = response.meta['kw']

        if response.status == 301:
            # 搜索无结果
            item = G7K7KItem()
            item['kw'] = kw
            item['result_count'] = '0'
            item['game_name'] = empty_word
            item['game_link'] = empty_word
            item['publish_time'] = empty_word
            item['game_logo'] = empty_word
            item['game_desc'] = empty_word
            item['game_tag'] = empty_word

            yield item

        elif response.status == 200:
            res_null = response.xpath('//div[@class="s_box"]/div/@class').extract()
            if 'search_null' in res_null:
                # 搜索无结果
                item = G7K7KItem()
                item['kw'] = kw
                item['result_count'] = '0'
                item['game_name'] = empty_word
                item['game_link'] = empty_word
                item['publish_time'] = empty_word
                item['game_logo'] = empty_word
                item['game_desc'] = empty_word
                item['game_tag'] = empty_word

                yield item

            else:
                result_count = response.xpath('//div[@class="s_box search_result"]/div[@class="box_hd"]/span/strong/text()').extract_first()
                results = response.xpath('//div[@class="s_box search_result"]/div/ul/li')
                for result in results:
                    item = G7K7KItem()
                    game_logo = result.xpath('./a/img/@src').extract_first()
                    game_name = result.xpath('./div[@class="game_name"]/a').extract_first()
                    game_name = re.compile(r'target="_blank">(.*)</a>').findall(game_name)[0].replace('<font color="red">', '').replace('</font>', '')
                    game_link = result.xpath('./div[@class="game_name"]/a/@href').extract_first()
                    publish_time = result.xpath('./div[@class="game_name"]/i/text()').extract_first()
                    game_desc = result.xpath('./p[@class="game_info"]').extract_first().replace('\r\n', '').replace('<font color="red">', '').replace('</font>', '')
                    game_tags = result.xpath('./dl/dd/a/text()').extract()
                    game_tag = ' '.join(game_tags)

                    item['kw'] = kw
                    item['result_count'] = result_count
                    item['game_name'] = game_name
                    item['game_link'] = game_link
                    item['publish_time'] = publish_time
                    item['game_logo'] = game_logo
                    item['game_desc'] = game_desc
                    item['game_tag'] = game_tag

                    yield item

                if int(result_count) > 21:
                    pages = int(int(result_count) / 21) + 1
                    for page in range(pages):
                        #          http://so.7k7k.com/game/%E7%8E%8B/click/1/0/0/-1/0/1/66.htm
                        new_url = 'http://so.7k7k.com/game/{}/click/1/0/0/-1/0/1/{}.htm'.format(quote(kw), str(page))
                        yield scrapy.Request(url=new_url, callback=self.parse_other_pages, meta={'kw': kw, 'result_count': result_count})

    def parse_other_pages(self, response):

        kw = response.meta['kw']
        result_count = response.meta['result_count']

        results = response.xpath('//div[@class="s_box search_result"]/div/ul/li')
        for result in results:
            item = G7K7KItem()
            game_logo = result.xpath('./a/img/@src').extract_first()
            game_name = result.xpath('./div[@class="game_name"]/a').extract_first()
            game_name = re.compile(r'target="_blank">(.*)</a>').findall(game_name)[0].replace('<font color="red">',
                                                                                              '').replace('</font>', '')
            game_link = result.xpath('./div[@class="game_name"]/a/@href').extract_first()
            publish_time = result.xpath('./div[@class="game_name"]/i/text()').extract_first()
            game_desc = result.xpath('./p[@class="game_info"]').extract_first().replace('\r\n', '').replace(
                '<font color="red">', '').replace('</font>', '')
            game_tags = result.xpath('./dl/dd/a/text()').extract()
            game_tag = ' '.join(game_tags)

            item['kw'] = kw
            item['result_count'] = result_count
            item['game_name'] = game_name
            item['game_link'] = game_link
            item['publish_time'] = publish_time
            item['game_logo'] = game_logo
            item['game_desc'] = game_desc
            item['game_tag'] = game_tag

            yield item

