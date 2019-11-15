# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HerostartItem(scrapy.Item):
    # 属于哪个类型下的
    product_type = scrapy.Field()
    # 所属公司
    belong_company = scrapy.Field()
    # 公司主营
    company_major = scrapy.Field()
    # 联系人
    linkman = scrapy.Field()
    # 电话号码
    tel = scrapy.Field()
    # 地址
    address = scrapy.Field()
