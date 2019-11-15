# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import scrapy
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class XinbdItem(scrapy.Item):
    # (entLogo, shareLogo, entName, bdCode, openStatus, entType, isClaim, claimUrl, benchMark, regNo, orgNo,
    #  taxNo, scope, regAddr, legalPerson, startDate, openTime, annualDate, regCapital, industry, telephone,
    #  district, authority, realCapital, orgType, scale, directors, shares, districtCode, cid, website,
    #  official_flag, shidi_pic, gongzhonghao, xiongzhanghao, weibo, phoneArr, baozhang_flag, shidi_flag,
    #  zixin_flag, chengqi_flag, v_level, v_url)
    search_kw = scrapy.Field()
    entLogo = scrapy.Field()
    shareLogo = scrapy.Field()
    entName = scrapy.Field()
    pid = scrapy.Field()
    tot = scrapy.Field()
    bdCode = scrapy.Field()
    openStatus = scrapy.Field()
    entType = scrapy.Field()
    isClaim = scrapy.Field()
    claimUrl = scrapy.Field()
    benchMark = scrapy.Field()
    regNo = scrapy.Field()
    orgNo = scrapy.Field()
    taxNo = scrapy.Field()
    scope = scrapy.Field()
    regAddr = scrapy.Field()
    legalPerson = scrapy.Field()
    startDate = scrapy.Field()
    openTime = scrapy.Field()
    annualDate = scrapy.Field()
    regCapital = scrapy.Field()
    industry = scrapy.Field()
    telephone = scrapy.Field()
    district = scrapy.Field()
    authority = scrapy.Field()
    realCapital = scrapy.Field()
    orgType = scrapy.Field()
    scale = scrapy.Field()
    directors = scrapy.Field()
    shares = scrapy.Field()
    districtCode = scrapy.Field()
    cid = scrapy.Field()
    website = scrapy.Field()
    official_flag = scrapy.Field()
    shidi_pic = scrapy.Field()
    gongzhonghao = scrapy.Field()
    xiongzhanghao = scrapy.Field()
    weibo = scrapy.Field()
    phoneArr = scrapy.Field()
    baozhang_flag = scrapy.Field()
    shidi_flag = scrapy.Field()
    zixin_flag = scrapy.Field()
    chengqi_flag = scrapy.Field()
    v_level = scrapy.Field()
    v_url = scrapy.Field()
