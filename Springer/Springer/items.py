# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpringerItem(scrapy.Item):
    search_kw = scrapy.Field()
    need = scrapy.Field()
    year = scrapy.Field()
    page = scrapy.Field()
    p_index = scrapy.Field()
    status = scrapy.Field()
    # journal_title = scrapy.Field()
    # articleCitation_year = scrapy.Field()
    # articleCitation_volume = scrapy.Field()
    # articleCitation_issue = scrapy.Field()
    # articleCitation_pages = scrapy.Field()
    # article_title = scrapy.Field()
    # # test_contributor_names = scrapy.Field()
    # contributor_names = scrapy.Field()
    # affiliations = scrapy.Field()
    # downloads = scrapy.Field()
    # citations = scrapy.Field()
    # abstract = scrapy.Field()
    # keywords = scrapy.Field()
    # refSource = scrapy.Field()
    # references = scrapy.Field()
