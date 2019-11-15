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


class RelationItem(scrapy.Item):

    # withOppoRelations 页面的字段
    commonDescriptor = scrapy.Field()
    entity = scrapy.Field()
    oppoPermissions = scrapy.Field()
    permissions = scrapy.Field()
    relations = scrapy.Field()

    # 增加一个页码判断
    nums = scrapy.Field()


class DocumentItem(scrapy.Item):
    # 增加一个页码判断
    nums = scrapy.Field()
    # withDocuments 页面的字段
    aaData = scrapy.Field()
    iTotalDisplayRecords = scrapy.Field()
    iTotalRecords = scrapy.Field()
    sEcho = scrapy.Field()


class TimelineItem(scrapy.Item):
    # 增加一个页码判断
    nums = scrapy.Field()
    # timeline 页面的字段
    actualDate = scrapy.Field()
    actualDateLabel = scrapy.Field()
    actualStatusLabel = scrapy.Field()
    milestones = scrapy.Field()
    totalSteps = scrapy.Field()


class CommunicationsItem(scrapy.Item):
    # 增加一个页码判断
    nums = scrapy.Field()
    # communications 页面的字段
    ctm = scrapy.Field()


class ImgItem(scrapy.Item):

    # 增加一个页码判断
    nums = scrapy.Field()

    # 图片保存的路径
    img_path = scrapy.Field()

    # 保存图片的名称
    img_name = scrapy.Field()
