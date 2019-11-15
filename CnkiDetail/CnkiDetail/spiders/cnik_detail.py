# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

from CnkiDetail.items import CnkidetailItem


class CnikDetailSpider(RedisSpider):
    name = 'cnik_detail'
    allowed_domains = ['cnki.net']
    start_urls = ['https://cnki.net/']
    redis_key = 'cnki:start_urls'

    def parse(self, response):
        # 在这url从其他地方取的，这里给一条静态的只是参考
        url = 'http://dbpub.cnki.net/grid2008/dbpub/detail.aspx?dbcode=SCPD&dbname=SCPD0809&filename=CN101751420A'
        yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = CnkidetailItem()
        tr = response.xpath("//table[@id='box']/tr")
        data = dict()
        data['link'] = response.url
        for td in tr:
            td_ls = td.xpath("./td/text()").extract()
            if len(td_ls) == 4:
                data[td_ls[0].replace("【", "").replace("】", "").strip()] = td_ls[1].replace("'", "’").replace(":",
                                                                                                              "：").strip()
                data[td_ls[2].replace("【", "").replace("】", "").strip()] = td_ls[3].replace("'", "’").replace(":",
                                                                                                              "：").strip()
            elif len(td_ls) == 2:
                data[td_ls[0].replace("【", "").replace("】", "").strip()] = td_ls[1].replace("'", "’").replace(":",
                                                                                                              "：").strip()
        kw_ls = ["link", "申请号", "申请日", "公开号", "公开日", "申请人", "地址", "共同申请人", "发明人", "国际申请",
                 "国际公布", "进入国家日期", "专利代理机构", "代理人", "分案原申请号", "国省代码", "摘要", "主权项", "页数",
                 "主分类号", "专利分类号"]
        for kw in kw_ls:
            if kw not in data:
                data[kw] = '""'

        item['link'] = data['link']
        item['apply_no'] = data['申请号']
        item['apply_day'] = data['申请日']
        item['pub_no'] = data['公开号']
        item['pub_day'] = data['公开日']
        item['applyer'] = data['申请人']
        item['address'] = data['地址']
        item['co_applyer'] = data['共同申请人']
        item['inventor'] = data['发明人']
        item['internal_apply'] = data['国际申请']
        item['internal_pub'] = data['国际公布']
        item['comming_data'] = data['进入国家日期']
        item['agency'] = data['专利代理机构']
        item['agent'] = data['代理人']
        item['origin_apply_no'] = data['分案原申请号']
        item['provicial_code'] = data['国省代码']
        item['abstract'] = data['摘要'].replace("\r", "").replace("\n", "")
        item['sovereignty'] = data['主权项'].replace("\r", "").replace("\n", "")
        item['pages'] = data['页数']
        item['main_class_no'] = data['主分类号']
        item['patent_class_no'] = data['专利分类号']

        yield item
