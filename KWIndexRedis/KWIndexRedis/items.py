# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KwindexItem(scrapy.Item):
    kw = scrapy.Field()
    sum_index = scrapy.Field()
    sum_index_change = scrapy.Field()
    baidu_pc_index = scrapy.Field()
    baidu_pc_index_change = scrapy.Field()
    baidu_mb_index = scrapy.Field()
    baidu_mb_index_change = scrapy.Field()
    index_360 = scrapy.Field()
    index_360_change = scrapy.Field()
    sougou_pc_index = scrapy.Field()
    sougou_pc_index_change = scrapy.Field()
    sougou_mb_index = scrapy.Field()
    sougou_mb_index_change = scrapy.Field()
    wechat_index = scrapy.Field()
    wechat_index_change = scrapy.Field()
    shenma_index = scrapy.Field()
    shenma_index_change = scrapy.Field()
