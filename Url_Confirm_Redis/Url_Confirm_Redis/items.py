# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlConfirmItem(scrapy.Item):
    # 搜索关键字
    kw = scrapy.Field()
    # 检索的网域
    domain = scrapy.Field()
    # 主办单位名称
    company_name = scrapy.Field()
    # 主办单位性质
    company_type = scrapy.Field()
    # 网站备案/许可证号
    company_no = scrapy.Field()
    # 网站名称
    company_web_name = scrapy.Field()
    # 网站首页网址
    company_url = scrapy.Field()
    # 审核时间
    check_time = scrapy.Field()
    # 以下信息更新时间
    update_time = scrapy.Field()
