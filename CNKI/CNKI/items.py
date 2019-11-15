# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnkiItem(scrapy.Item):
    # keyword 检索的关键字
    kw = scrapy.Field()
    # 搜索出专利所在的序号
    c_no = scrapy.Field()
    # 专利的名称
    name = scrapy.Field()
    # 发明人
    inventor = scrapy.Field()
    # 申请人
    applicant = scrapy.Field()
    # 来源数据库
    source_from = scrapy.Field()
    # 申请日
    apply_date = scrapy.Field()
    # 公开日
    pub_date = scrapy.Field()
    # 网页链接
    link = scrapy.Field()
