# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuliveItem(scrapy.Item):
    # 搜索关键字
    kw = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 讲者
    speakers_name = scrapy.Field()
    # live 的网址
    target_url = scrapy.Field()
    # 评星
    estimation = scrapy.Field()
    # 参与人数
    taken = scrapy.Field()
    # 这个ID是我用来判断前五个的, 后面的为真实ID
    zh_id = scrapy.Field()
