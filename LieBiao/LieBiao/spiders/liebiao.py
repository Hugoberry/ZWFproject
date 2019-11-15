# -*- coding: utf-8 -*-
import scrapy


class LiebiaoSpider(scrapy.Spider):
    name = 'liebiao'
    allowed_domains = ['liebiao.com']
    start_urls = ['http://liebiao.com/']

    def parse(self, response):
        pass
