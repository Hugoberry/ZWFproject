# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Game9Item(scrapy.Item):
    kw = scrapy.Field()
    game_name = scrapy.Field()
    game_link = scrapy.Field()
    game_logo = scrapy.Field()
    game_data_type = scrapy.Field()
    game_desc = scrapy.Field()
