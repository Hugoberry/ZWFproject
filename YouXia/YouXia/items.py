# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YouxiaItem(scrapy.Item):
    # 关键字
    game_kw = scrapy.Field()
    # 游戏名称
    game_name = scrapy.Field()
    # 游戏类型
    game_type = scrapy.Field()
    # 游戏在游侠网的链接
    game_url = scrapy.Field()
    # 游戏的图片链接
    game_img_url = scrapy.Field()


class YouxiaDownloadItem(scrapy.Item):
    # 关键字
    game_kw = scrapy.Field()
    # 下载的标题
    download_title = scrapy.Field()
    # 下载地址
    download_url = scrapy.Field()
    # 文件大小
    file_size = scrapy.Field()
    # 发布时间
    publish_time = scrapy.Field()
    # 描述
    describe = scrapy.Field()
