# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CzvvScrapyItem(scrapy.Item):
    # 标题（大多数标题是公司的名称）
    title = scrapy.Field()
    # 企业简介
    company_intro = scrapy.Field()
    # 联系方式
    contact_information = scrapy.Field()
    # 经营范围
    business_scope = scrapy.Field()
    # 工商档案
    commercial_archives = scrapy.Field()
    # 商标信息(商标名称)
    trade_mark_info = scrapy.Field()
    # 产品及服务
    # product_server = scrapy.Field()
