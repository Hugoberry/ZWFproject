# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Search360Item(scrapy.Item):
    kw = scrapy.Field()
    search_nums = scrapy.Field()
