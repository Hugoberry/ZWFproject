# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
import re
from Search360.items import Search360Item


class Sear360Spider(scrapy.Spider):
    name = 'sear_360'
    allowed_domains = ['so.com']
    start_urls = ['https://www.so.com/']

    def parse(self, response):
        file = open(r'./a.txt', 'r+')
        line = file.readlines()
        len_len = len(line)
        for word in range(len_len):
            kw = line[word].replace('(', '').replace(',1)', '').strip()
            print(kw)
            item = Search360Item()
            item['kw'] = kw
            search_url = response.url + 's?ie=utf-8&fr=none&src=360sou_newhome&q=%s' % quote(kw)
            yield scrapy.Request(url=search_url, callback=self.parse_search, meta={'item': item})

    def parse_search(self, response):
        item = response.meta['item']
        search_nums_str = response.xpath('//div[@id="page"]/span[@class="nums"]/text()').extract_first()
        search_nums = re.compile('找到相关结果约(.*?)个').findall(search_nums_str)[0]
        item['search_nums'] = search_nums
        news_url = 'https://news.so.com/ns?q=%s&src=newhome' % item['kw']
        yield scrapy.Request(url=news_url, callback=self.parse_news, meta={'item': item})

    def parse_news(self, response):
        item = response.meta['item']
        news_nums_str = response.xpath('//div[@class="filter-total"]/text()').extract_first()
        news_nums = re.compile(r'为您推荐相关资讯约(.*?)条').findall(news_nums_str)[0]
        item['news_nums'] = news_nums
        yield item
