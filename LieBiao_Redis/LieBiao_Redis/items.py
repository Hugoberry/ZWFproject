# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiebiaoItem(scrapy.Item):
    # 来源网站链接
    url_link = scrapy.Field()
    # 列表网的标题
    title = scrapy.Field()
    # 创建时间
    create_data = scrapy.Field()
    # 浏览量
    # view_num = scrapy.Field()
    # 公司名称
    company_name = scrapy.Field()
    # 公司类型
    company_type = scrapy.Field()
    # 公司位置
    company_position = scrapy.Field()
    # 认证情况
    clarify_situation = scrapy.Field()
    # 联系人
    linkman = scrapy.Field()
    # 微信号码
    wechat = scrapy.Field()
    # QQ号码
    qq = scrapy.Field()
    # 电话号码
    tel_no = scrapy.Field()
    # 详情描述
    detail = scrapy.Field()
    # 关键字
    key_word = scrapy.Field()
