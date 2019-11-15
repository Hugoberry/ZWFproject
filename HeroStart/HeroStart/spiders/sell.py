# -*- coding: utf-8 -*-
import re

import scrapy

from HeroStart.items import HerostartItem


class SellSpider(scrapy.Spider):
    name = 'sell'
    allowed_domains = ['china.herostart.com']
    start_urls = ['http://china.herostart.com/sell/']

    def parse(self, response):
        # 所有的分类table
        all_table = response.xpath('//div[@class="left_box"]/div[@class="catalog"]/table')
        for table in all_table:
            # 所有的链接
            all_title = table.xpath('.//tr/td[2]/p/a/@href').extract()
            for title in all_title:
                url = 'http://china.herostart.com' + title
                yield scrapy.Request(url=url, callback=self.parse_title)

    def parse_title(self, response):
        # 产品的类型
        product_type = response.xpath('//div[@class="way"]/a[2]/text()').extract_first() + ': ' + response.xpath('//div[@class="way"]/a[3]/text()').extract_first()
        # 所有类别的细分
        all_category = response.xpath('//div[@class="relacats "]//ul/li/a/@href').extract()
        for category in all_category:
            url = 'http://china.herostart.com' + category
            yield scrapy.Request(url=url, callback=self.parse_list, meta={'product_type': product_type})

    def parse_list(self, response):
        product_type = response.meta['product_type']
        # 解析列表页
        all_url = response.xpath('//ul[@class="piclist"]/li//h3/a/@href').extract()
        for url in all_url:
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'product_type': product_type})

        next_url = response.xpath('//div[@class="pages"]/a[2]/@href').extract_first()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse_list2, meta={'product_type': product_type})

    def parse_list2(self, response):
        product_type = response.meta['product_type']

        all_url = response.xpath('//ul[@class="piclist"]/li//h3/a/@href').extract()
        for url in all_url:
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'product_type': product_type})

        all_pages = response.xpath('//div[@class="pages"]/cite/text()').extract_first()
        all_pages = re.compile('共\d+条/(\d+)页').findall(all_pages)
        if all_pages:
            all_pages = int(all_pages[0])
            url_key = re.compile(r'com/k/(.*)-2\.html').findall(response.url)[0]
            for x in range(3, all_pages + 1):
                url = 'http://china.herostart.com/k/' + url_key + '-' + str(x) + '.html'
                yield scrapy.Request(url=url, callback=self.parse_detail, meta={'product_type': product_type})

    def parse_detail(self, response):
        product_type = response.meta['product_type']

        table = response.xpath('//table[@cellspacing="5"]')
        for info in table:
            item = HerostartItem()
            belong_company = info.xpath('.//tr[1]/td[2]/b/a/text()').extract_first()
            company_major = info.xpath('.//tr[2]/td[2]/text()').extract_first()
            linkman = info.xpath('.//tr[3]/td[2]/text()').extract_first()
            tel = '; '.join(info.xpath('.//tr[4]/td[2]/em/text()').extract())
            address = info.xpath('.//tr[last()]/td[2]/text()').extract_first()
            item['product_type'] = product_type
            item['belong_company'] = belong_company
            item['company_major'] = company_major
            item['linkman'] = linkman
            item['tel'] = tel
            item['address'] = address
            yield item
