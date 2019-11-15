# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SipoppolicyItem(scrapy.Item):
    area = scrapy.Field()
    areaCode = scrapy.Field()
    attachmentLocalUrl = scrapy.Field()
    attachmentName = scrapy.Field()
    city = scrapy.Field()
    cityCode = scrapy.Field()
    createUserName = scrapy.Field()
    declarAcceptOrg = scrapy.Field()
    declarAcceptOrgAddress = scrapy.Field()
    declarAcceptTelephone = scrapy.Field()
    declarBeginTime = scrapy.Field()
    declarConsultMail = scrapy.Field()
    declarContent = scrapy.Field()
    declarContentKeyWord = scrapy.Field()
    declarDispatchTime = scrapy.Field()
    declarEndTime = scrapy.Field()
    declarMail = scrapy.Field()
    declarObject = scrapy.Field()
    declarOrgZipcode = scrapy.Field()
    declarRequire = scrapy.Field()
    declarTopicName = scrapy.Field()
    declarUrl = scrapy.Field()
    handleState = scrapy.Field()
    this_id = scrapy.Field()
    isHaveAttachment = scrapy.Field()
    isRefuse = scrapy.Field()
    orgAddress = scrapy.Field()
    orgTelephone = scrapy.Field()
    organization = scrapy.Field()
    originalLastWebSite = scrapy.Field()
    policyId = scrapy.Field()
    policyIds = scrapy.Field()
    policyNames = scrapy.Field()
    projectDeclarType = scrapy.Field()
    projectId = scrapy.Field()
    projectName = scrapy.Field()
    province = scrapy.Field()
    provinceCode = scrapy.Field()
    region = scrapy.Field()
    releaseDate = scrapy.Field()
    remark = scrapy.Field()
