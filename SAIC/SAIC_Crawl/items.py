# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SaicCrawlItem(scrapy.Item):
    # 这是列表页的字段
    # 案件标题
    title = scrapy.Field()
    # 在商标评审委员会的链接
    link = scrapy.Field()
    # 日期
    date = scrapy.Field()
    # 裁决类型
    judge_type = scrapy.Field()

    # 详情页的信息
    # 案件号码
    case_no = scrapy.Field()
    # 申请人
    applicator = scrapy.Field()
    # 被申请人
    by_applicator = scrapy.Field()
    # 委托代理人
    proxies = scrapy.Field()
    # 案例商标
    case_icon = scrapy.Field()
    # 案例商标对于的链接
    case_icon_link = scrapy.Field()
    # 裁定依据
    judge_relay = scrapy.Field()
    # 合议组成员
    member = scrapy.Field()
    # 成功失败
    judge_status = scrapy.Field()
    # 服务范围
    server_range = scrapy.Field()

    # 裁决书内容
    pg_content = scrapy.Field()
