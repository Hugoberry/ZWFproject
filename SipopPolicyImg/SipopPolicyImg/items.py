# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SipoppolicyItem(scrapy.Item):
    area = scrapy.Field()
    areaCode = scrapy.Field()
    city = scrapy.Field()
    cityCode = scrapy.Field()
    graphicId = scrapy.Field()
    graphicTitle = scrapy.Field()
    graphicType = scrapy.Field()
    this_id = scrapy.Field()
    originalLastWebSite = scrapy.Field()
    policyContent = scrapy.Field()
    policyContentUrl = scrapy.Field()
    policyId = scrapy.Field()
    policyOrg = scrapy.Field()
    province = scrapy.Field()
    provinceCode = scrapy.Field()
    publishTime = scrapy.Field()
    region = scrapy.Field()
    releaseDate = scrapy.Field()
