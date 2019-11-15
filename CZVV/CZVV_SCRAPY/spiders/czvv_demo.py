# -*- coding: utf-8 -*-
import re
# import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from CZVV_SCRAPY.items import CzvvScrapyItem

empty_word = 'null'


class CzvvDemoSpider(CrawlSpider):
    name = 'czvv_demo'
    allowed_domains = ['czvv.com']
    start_urls = ['http://www.czvv.com/huangye/10298320.html']

    rules = (
        Rule(LinkExtractor(allow=r'huangye/\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        item = CzvvScrapyItem()
        all_info = response.xpath('//div[@class="col-sm-12"]')
        title_set = set()

        company_title = response.xpath('//div[@class="col-xs-12 col-sm-10"]/div[@class="col-sm-12 Title"]/h2/text()').extract_first()
        item['title'] = company_title
        title_set.add('title')

        for info in all_info:

            title = ''
            try:
                title = info.xpath('./div[@class="title"]').extract_first().strip()
            except AttributeError:
                pass

            if '企业简介' in title:
                company_intro = info.xpath('./div[@class="word"]/div[@class="inbox"]/text()').extract()
                company_intro = (''.join(company_intro)).strip()
                item['company_intro'] = company_intro
                title_set.add('company_intro')

            elif '联系方式' in title:
                contact_information = info.xpath('./div[@class="col-sm-12"]/span[@class="col-sm-6 form-group"]').extract()
                contact_information = (', '.join(contact_information)).strip().replace('\n', '')
                re_ls = re.compile('<span.*?class="col-sm-3 text-muted">(.*?)</span>(.*?)</span>').findall(contact_information)
                need_info = []
                for ni in re_ls:
                    # if ni[0] not in ['邮箱', '商铺', '网址']:
                    if '邮箱' in ni[0]:
                        pass
                    elif '商铺' in ni[0]:
                        pass
                    elif '网址' in ni[0]:
                        pass
                    else:
                        nw = ''.join(ni).strip()
                        need_info.append(nw)
                need_info = ', '.join(need_info)
                item['contact_information'] = need_info
                title_set.add('contact_information')

            elif '工商档案' in title:
                # TODO http://www.czvv.com/huangye/10086.html (以这个网页为原型解析)
                ic_info = info.xpath('./div[@class="col-sm-6"]/div[@class="col-sm-12"]')
                ic_ls = []
                for ic in ic_info:
                    ic_title = ic.xpath('./div[@class="col-sm-3 titlebox"]/text()').extract_first().strip()
                    ic_content = ic.xpath('./div[@class="col-sm-9"]/text()').extract_first().strip()
                    if '传众征信' in ic_title:
                        pass
                    else:
                        ic_ls.append(ic_title + ic_content)
                item['commercial_archives'] = ', '.join(ic_ls)
                title_set.add('commercial_archives')

            elif '经营范围' in title:
                business_scope = info.xpath('./p[@class="col-sm-12"]/text()').extract_first().strip()
                item['business_scope'] = business_scope
                title_set.add('business_scope')

            elif '商标信息' in title:
                trade_mark_info = info.xpath('./div[@class="col-sm-12 product_a"]/a/span/text()').extract_first().strip()
                item['trade_mark_info'] = trade_mark_info
                title_set.add('trade_mark_info')

        title_all = {'title', 'company_intro', 'contact_information', 'business_scope', 'commercial_archives', 'trade_mark_info'}
        print(type(title_all))

        title_null = title_all - title_set

        for n_t in title_null:
            item[n_t] = empty_word

        yield item
