# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchItem(scrapy.Item):
    kw = scrapy.Field()
    search_nums = scrapy.Field()
    news_nums = scrapy.Field()
