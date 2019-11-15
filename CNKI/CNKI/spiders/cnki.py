# -*- coding: utf-8 -*-
import re
import time
from urllib.parse import quote

import scrapy

from CNKI.items import CnkiItem


class CnkiSpider(scrapy.Spider):
    name = 'cnki'
    allowed_domains = ['cnki.net']
    start_urls = ['http://cnki.net/']

    def parse(self, response):
        file = open('./cnki_kw.txt', mode='r+', encoding='utf-8')
        while True:
            lines = file.readlines(4096)
            if not lines:
                break
            for line in lines:
                kw = line.replace("\n", "")

                data = {
                    'action': '',
                    'ua': '1.11',
                    'isinEn': '0',
                    'PageName': 'ASP.brief_default_result_aspx',
                    'DbPrefix': 'SCOD',
                    'DbCatalog': '中国学术文献网络出版总库',
                    'ConfigFile': 'SCDBINDEX.xml',
                    'db_opt': 'SCOD',
                    'txt_1_sel': 'SU$%=|',
                    'txt_1_value1': '%s' % kw,
                    'txt_1_special1': '%',
                    'his': '0',
                    'parentdb': 'SCDB',
                }
                post_url = "https://kns.cnki.net/kns/request/SearchHandler.ashx"

                yield scrapy.FormRequest(url=post_url, formdata=data, callback=self.parse_post, meta={'kw': kw})

    def parse_post(self, response):
        kw = response.meta['kw']
        url_str = response.text
        cnki_url = "https://kns.cnki.net/kns/brief/brief.aspx?pagename=%s&t=%d&keyValue=%s&S=1&sorttype=" % (
            url_str, int(time.time() * 1000), quote(kw))
        # yield scrapy.Request(url=cnki_url, callback=self.parse_urls, meta={'kw': kw})
        yield scrapy.Request(url=cnki_url, callback=self.parse_list, meta={'kw': kw})

    def parse_list(self, response):
        referer = response.url
        pages = response.xpath("//span[@class='countPageMark']/text()").extract_first().replace("1/", "")
        for page in range(2, int(pages) + 1):
            url = "https://kns.cnki.net/kns/brief/brief.aspx?curpage=%d&RecordsPerPage=20&QueryID=3&ID=&turnpage=1" \
                  "&tpagemode=L&dbPrefix=SCOD&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx" \
                  "&sKuaKuID=3&isinEn=0&" % page
            headers = {
                'Referer': referer,
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse_urls, meta={'kw': response.meta['kw']})

    def parse_urls(self, response):
        kw = response.meta['kw']
        tr = response.xpath('//tr[@bgcolor="#ffffff"] | //tr[@bgcolor="#f6f7fb"]')
        for td in tr:
            item = CnkiItem()
            c_no = td.xpath('./td[1]/text()').extract_first()
            name = td.xpath('./td[2]/a').extract_first()
            name = re.compile(r'target="_blank">(.*?)</a>').findall(name)[0].replace('<font class="Mark">', "").replace('</font>', "")
            url_dict = dict()
            url_param = td.xpath('./td[2]/a/@href').extract_first().split("&")
            for u in url_param:
                if 'dbcode' in u:
                    url_dict['dbcode'] = u
                elif 'dbname' in u:
                    url_dict['dbname'] = u
                elif 'filename' in u:
                    url_dict['filename'] = u
            link = "http://dbpub.cnki.net/grid2008/dbpub/detail.aspx?" + url_dict['dbcode'] + "&" + url_dict['dbname']\
                   + "&" + url_dict['filename']
            inventor = td.xpath('./td[3]/text()').extract_first()
            applicant = td.xpath('./td[4]/text()').extract_first()
            source_from = td.xpath('./td[5]/text()').extract_first()
            apply_date = td.xpath('./td[6]/text()').extract_first()
            pub_date = td.xpath('./td[7]/text()').extract_first()

            item['kw'] = kw
            item['c_no'] = c_no
            item['name'] = name
            item['link'] = link
            item['inventor'] = inventor
            item['applicant'] = applicant
            item['source_from'] = source_from
            item['apply_date'] = apply_date
            item['pub_date'] = pub_date
            yield item
