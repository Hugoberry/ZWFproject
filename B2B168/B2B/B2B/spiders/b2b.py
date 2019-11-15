# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from B2B.items import B2BItem


class B2bSpider(CrawlSpider):
    name = 'b2b'
    allowed_domains = ['info.b2b168.com']
    start_urls = ['https://info.b2b168.com/s168-109115216.html']

    rules = (
        Rule(LinkExtractor(allow=r'com/s168-\d+\.html$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        item = B2BItem()
        item['source_from'] = response.url

        info = response.xpath('//div[@class="ptlxfsC"]/ul[1]')
        for data in info:
            company_name = data.xpath('./h1/text()').extract_first()
            item['company_name'] = company_name
            person_name = data.xpath('./li[1]/strong/a/text()').extract_first()
            item['person_name'] = person_name
            others = data.xpath('./li[1]/p')
            for oth in others:
                if '电话' in oth.xpath('./text()').extract_first():
                    tel = oth.xpath('./text()').extract_first()
                    item['tel'] = tel
                elif '地址' in oth.xpath('./text()').extract_first():
                    a_text = oth.xpath('./a/text()').extract()
                    address = oth.xpath('./text()').extract()
                    address = ''.join(address).replace('地址：', '')
                    a_text.append(address)
                    address = ' '.join(a_text)
                    item['address'] = address
                elif '手机' in oth.xpath('./text()').extract_first():
                    mob = oth.xpath('./text()').extract_first()
                    item['mob'] = mob
                elif 'QQ' in oth.xpath('./text()').extract_first():
                    qq = oth.xpath('./text()').extract_first()
                    item['qq'] = qq
                elif '邮件' in oth.xpath('./text()').extract_first():
                    mail = oth.xpath('./text()').extract_first()
                    item['mail'] = mail
                elif '传真' in oth.xpath('./text()').extract_first():
                    fax = oth.xpath('./text()').extract_first()
                    item['fax'] = fax
                elif '邮编' in oth.xpath('./text()').extract_first():
                    zip_code = oth.xpath('./text()').extract_first()
                    item['zip_code'] = zip_code
                elif '网址' in oth.xpath('./text()').extract_first():
                    website = oth.xpath('./text()').extract_first()
                    item['website'] = website
                else:
                    pass
        yield item
