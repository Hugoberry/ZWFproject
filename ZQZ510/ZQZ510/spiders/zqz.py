# -*- coding: utf-8 -*-
import scrapy
import time
import json

from ZQZ510.items import Zqz510Item

empty_word = 'null'


class ZqzSpider(scrapy.Spider):
    name = 'zqz'
    allowed_domains = ['zqz510.com']
    start_urls = ['http://login.zqz510.com/judgmentDoc']

    def parse(self, response):
        url = 'http://api.zqz510.com//tmof/query?ftxt=&ti=&apS=&pdStart=&pdEnd=&ty=&psty=&law=&litem=&pageNum=1' \
              '&apS=&apD=&ag=&judgd=&tid=&cid=&callback=_jqjsp&_{}='.format(str(int(time.time() * 1000)))
        self.cookie = {
            'uid': '213facea-5ac7-4069-ae4a-97168d559ebc',
            'oid': 'UAGAP00003919',
            'JSESSIONID': '9867C3C37D24634CB9D44D1AA5C6188F',
            'c': '82f5dd5f-f8ae-459b-9907-fd0bb01d97cb',
        }
        yield scrapy.Request(url=url, callback=self.parse_first, cookies=self.cookie)

    def parse_first(self, response):

        json_text = json.loads(response.text[7:-1], encoding='utf-8')
        total = int(json_text['total'])
        all_page = int(total / 10) + 1
        for page in range(all_page):
            url = 'http://api.zqz510.com//tmof/query?ftxt=&ti=&apS=&pdStart=&pdEnd=&ty=&psty=&law=&litem=&pageNum={}' \
                  '&apS=&apD=&ag=&judgd=&tid=&cid=&callback=_jqjsp&_{}='.format(str(page + 1), str(int(time.time() * 1000)))
            yield scrapy.Request(url=url, callback=self.parse_list, cookies=self.cookie)

    def parse_list(self, response):
        json_text = json.loads(response.text[7:-1], encoding='utf-8')
        for data in json_text['data']:
            item = Zqz510Item()

            if 'agS' in data:
                item['agS'] = data['agS']
            else:
                item['agS'] = empty_word

            if 'agidS' in data:
                item['agidS'] = data['agidS']
            else:
                item['agidS'] = empty_word

            if 'an' in data:
                item['an'] = data['an']
            else:
                item['an'] = empty_word

            if 'anDest' in data:
                item['anDest'] = data['anDest']
            else:
                item['anDest'] = empty_word

            if 'anList' in data:
                item['anList'] = str(data['anList'])
            else:
                item['anList'] = empty_word

            if 'apS' in data:
                item['apS'] = data['apS']
            else:
                item['apS'] = empty_word

            if 'apidS' in data:
                item['apidS'] = data['apidS']
            else:
                item['apidS'] = empty_word

            if 'cid' in data:
                item['cid'] = data['cid']
            else:
                item['cid'] = empty_word

            if 'docid' in data:
                item['docid'] = data['docid']
            else:
                item['docid'] = empty_word

            if 'law' in data:
                item['law'] = data['law']
            else:
                item['law'] = empty_word

            if 'link' in data:
                item['link'] = data['link']
            else:
                item['link'] = empty_word

            if 'litem' in data:
                item['litem'] = data['litem']
            else:
                item['litem'] = empty_word

            if 'ltid' in data:
                item['ltid'] = data['ltid']
            else:
                item['ltid'] = empty_word

            if 'pd' in data:
                item['pd'] = data['pd']
            else:
                item['pd'] = empty_word

            if 'psty' in data:
                item['psty'] = data['psty']
            else:
                item['psty'] = empty_word

            if 'rid' in data:
                item['rid'] = data['rid']
            else:
                item['rid'] = empty_word

            if 'ti' in data:
                item['ti'] = data['ti']
            else:
                item['ti'] = empty_word

            if 'ty' in data:
                item['ty'] = data['ty']
            else:
                item['ty'] = empty_word

            detail_url = 'http://api.zqz510.com/tmof/detail?docid={}&callback=_jqjsp&_{}='.format(item['docid'], str(int(time.time() * 1000)))
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, meta={'item': item}, cookies=self.cookie)

    def parse_detail(self, response):
        json_text = json.loads(response.text[7:-1], encoding='utf-8')
        item = response.meta['item']

        if 'dtls' in json_text:
            item['dtls'] = str(json_text['dtls'])
        else:
            item['dtls'] = empty_word

        if 'ftxt' in json_text:
            item['ftxt'] = json_text['ftxt']
        else:
            item['ftxt'] = empty_word

        if 'judg' in json_text:
            item['judg'] = str(json_text['judg'])
        else:
            item['judg'] = empty_word

        if 'judgList' in json_text:
            item['judgList'] = str(json_text['judgList'])
        else:
            item['judgList'] = empty_word

        if 'links' in json_text:
            item['links'] = str(json_text['links'])
        else:
            item['links'] = empty_word

        if 'ltidAll' in json_text:
            item['ltidAll'] = str(json_text['ltidAll'])
        else:
            item['ltidAll'] = empty_word

        if 'pdCn' in json_text:
            item['pdCn'] = str(json_text['pdCn'])
        else:
            item['pdCn'] = empty_word

        yield item