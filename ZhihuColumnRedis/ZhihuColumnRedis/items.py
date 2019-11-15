# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihucolumnItem(scrapy.Item):
    # 需要查询的关键字
    kw = scrapy.Field()
    # 标题名称
    title = scrapy.Field()
    # 标题的介绍
    description = scrapy.Field()
    # 搜索的ID
    id_no = scrapy.Field()
    # 文章数
    articles_count = scrapy.Field()
    # 关注数量
    followers = scrapy.Field()
    # 商标图片链接
    avatar_url = scrapy.Field()
    # 创建者名字
    creator_name = scrapy.Field()
    # 创建者链接
    creator_url = scrapy.Field()
