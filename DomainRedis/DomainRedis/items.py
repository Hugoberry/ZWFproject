# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DomaintestItem(scrapy.Item):
    kw = scrapy.Field()
    domain_type = scrapy.Field()
    domain_url = scrapy.Field()
    domain_status = scrapy.Field()
