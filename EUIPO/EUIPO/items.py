# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EuipoItem(scrapy.Item):
    representativeid = scrapy.Field()
    basis = scrapy.Field()
    nice = scrapy.Field()
    numberToShow = scrapy.Field()
    publisheddate = scrapy.Field()
    # 这个原字段是type
    this_type = scrapy.Field()
    publishedsection = scrapy.Field()
    statusCode = scrapy.Field()
    milestone = scrapy.Field()
    thumbnailurl = scrapy.Field()
    name = scrapy.Field()
    commonDescriptor = scrapy.Field()
    applicantname = scrapy.Field()
    imageurl = scrapy.Field()
    designationdate = scrapy.Field()
    applicantsreference = scrapy.Field()
    publishedurl = scrapy.Field()
    registrationdate = scrapy.Field()
    status = scrapy.Field()
    applicantStatus = scrapy.Field()
    fastTrackIndicator = scrapy.Field()
    number = scrapy.Field()
    publications = scrapy.Field()
    filingdate = scrapy.Field()
    controller = scrapy.Field()
    applicantid = scrapy.Field()
    representativename = scrapy.Field()
