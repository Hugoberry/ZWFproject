# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Zqz510Item(scrapy.Item):
    agS = scrapy.Field()
    agidS = scrapy.Field()
    an = scrapy.Field()
    anDest = scrapy.Field()
    anList = scrapy.Field()
    apS = scrapy.Field()
    apidS = scrapy.Field()
    cid = scrapy.Field()
    docid = scrapy.Field()
    law = scrapy.Field()
    link = scrapy.Field()
    litem = scrapy.Field()
    ltid = scrapy.Field()
    pd = scrapy.Field()
    psty = scrapy.Field()
    rid = scrapy.Field()
    ti = scrapy.Field()
    ty = scrapy.Field()

    # 详情页
    dtls = scrapy.Field()
    ftxt = scrapy.Field()
    judg = scrapy.Field()
    judgList = scrapy.Field()
    links = scrapy.Field()
    ltidAll = scrapy.Field()
    pdCn = scrapy.Field()
