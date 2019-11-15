# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihutopicItem(scrapy.Item):
    # 需要查询的关键字
    kw = scrapy.Field()
    # 标题(话题的标题)
    title = scrapy.Field()
    # 话题logo
    avatar_url = scrapy.Field()
    # 描述(对于这段话题的描述)
    description = scrapy.Field()
    # 关注人数
    followers_count = scrapy.Field()
    # 搜索的ID
    id_no = scrapy.Field()
    # 问题数量
    questions_count = scrapy.Field()
    # 精华数量
    top_answer_count = scrapy.Field()
    #  话题链接
    topic_url = scrapy.Field()
