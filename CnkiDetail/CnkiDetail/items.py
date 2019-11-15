# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnkidetailItem(scrapy.Item):
    link = scrapy.Field()
    apply_no = scrapy.Field()
    apply_day = scrapy.Field()
    pub_no = scrapy.Field()
    pub_day = scrapy.Field()
    applyer = scrapy.Field()
    address = scrapy.Field()
    co_applyer = scrapy.Field()
    inventor = scrapy.Field()
    internal_apply = scrapy.Field()
    internal_pub = scrapy.Field()
    comming_data = scrapy.Field()
    agency = scrapy.Field()
    agent = scrapy.Field()
    origin_apply_no = scrapy.Field()
    provicial_code = scrapy.Field()
    abstract = scrapy.Field()
    sovereignty = scrapy.Field()
    pages = scrapy.Field()
    main_class_no = scrapy.Field()
    patent_class_no = scrapy.Field()
