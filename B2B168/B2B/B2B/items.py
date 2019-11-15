# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class B2BItem(scrapy.Item):
    company_name = scrapy.Field()
    person_name = scrapy.Field()
    tel = scrapy.Field()
    address = scrapy.Field()
    mob = scrapy.Field()
    qq = scrapy.Field()
    mail = scrapy.Field()
    fax = scrapy.Field()
    zip_code = scrapy.Field()
    website = scrapy.Field()
    source_from = scrapy.Field()
