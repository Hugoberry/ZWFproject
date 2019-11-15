# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

from LieBiao_Redis.items import LiebiaoItem

empty_word = 'null'


class RuleLiebiaoSpider(RedisCrawlSpider):
    name = 'liebiao_redis'
    allowed_domains = ['liebiao.com']
    redis_key = 'liebiao:start_urls'
    start_urls = ['http://beijing.liebiao.com/gongshangzhuce/']

    rules = (
        Rule(LinkExtractor(allow=r'http://beijing\.liebiao\.com/gongshangzhuce/\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = LiebiaoItem()
        item['url_link'] = response.url
        item['title'] = response.xpath('//div[@class="post-title"]/h1[@class="ellipsis"]/text()').extract_first()
        item['create_data'] = response.xpath('//div[@class="clf"]/div[@class="statistic"]/span[1]/text()').extract_first()
        # 浏览量在
        # item['view_num'] = response.xpath('//div[@class="clf"]/div[@class="statistic"]/span[2]/span[@id="post_visitors"]').extract_first()
        item['company_name'] = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/div/dl[1]/dd/a/text()').extract_first()
        # 在这是一个列表
        company_type = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/div/dl[2]/dd/a/text()').extract()
        item['company_type'] = str(company_type)

        # 公司所在的地址
        position_before = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/div/dl[3]/dd/a/text()').extract()
        position_after = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/div/dl[3]/dd/span/text()').extract()
        if position_after:
            item['company_position'] = ','.join(position_before) + ',' + position_after[0]
        else:
            item['company_position'] = ','.join(position_before)

        # 认证情况（列表）
        clarify = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/dl[1]/dd[@class="field-detail"]/i/@title').extract()
        item['clarify_situation'] = ','.join(clarify)

        # 联系人
        item['linkman'] = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/dl[2]/dd/span/text()').extract_first()

        # 微信扫码地址
        item['wechat'] = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/dl[2]/dd/div/ul/li/span/text()').extract_first()

        # QQ号码
        item['qq'] = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/dl[2]/dd/a[1]/@title').extract_first()

        # 电话号码
        item['tel_no'] = response.xpath('//div[@class="clf"]/div[@class="field-wrap"]/div[@class="contact-way-wrap"]/button[@class="btn-check-phone click_btn"]/@data-phone').extract_first()

        # 详情描述
        item['detail'] = response.xpath('//div[@class="content-wrap"]').extract_first()

        # 关键字(列表)
        item['key_word'] = ','.join(response.xpath('//div[@class="keyword-wrap"]/strong[@class="keyword"]/text()').extract())

        yield item
