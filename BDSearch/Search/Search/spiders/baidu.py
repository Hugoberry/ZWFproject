# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
import re
from Search.items import SearchItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        file = open(r'./a.txt', 'r+')
        line = file.readlines()
        len_len = len(line)
        for word in range(len_len):
            kw = line[word].replace('(', '').replace(',1)', '').strip()
            print(kw)
            item = SearchItem()
            item['kw'] = kw
            url = response.url + 's?wd=%s' % quote(kw)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        nums_str = response.xpath('//div[@class="nums"]/span/text()').extract_first()
        nums = re.compile(r'百度为您找到相关结果约(.*?)个').findall(nums_str)[0]
        item['search_nums'] = nums
        # 'https://www.baidu.com/s?tn=news&word=%E8%99%BE%E7%B1%B3'
        print(nums)
        news_url = 'http://news.baidu.com/ns?word=%s&tn=news&from=news&cl=2&rn=20&ct=1' % quote(item['kw'])
        print(news_url)
        yield scrapy.Request(url=news_url, callback=self.parse_news, meta={'item': item})

    def parse_news(self, response):
        item = response.meta['item']
        news_str = response.xpath('//div[@id="header_top_bar"]/span/text()').extract_first()
        news_nums = re.compile(r'找到相关新闻约(.*?)篇').findall(news_str)[0]
        print(news_nums)
        item['news_nums'] = news_nums
        yield item
