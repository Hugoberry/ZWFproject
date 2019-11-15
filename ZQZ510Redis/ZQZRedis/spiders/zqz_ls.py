# -*- coding: utf-8 -*-
import scrapy
import time
import json

from scrapy_redis.spiders import RedisSpider

from ZQZRedis.items import Zqz510Item

empty_word = 'null'


class ZqzSpider(RedisSpider):
    name = 'zqz_ls'
    allowed_domains = ['zqz510.com']
    start_urls = ['https://www.baidu.com']
    redis_key = 'zqz_ls:start_urls'

    cookie = {
        '_lastEnterDay': '2018-12-11',
        '_cliid': '5VvVudZ1LvXdy-13',
        '_siteStatId': '1f84349f-3e84-421f-bfe3-bdfdcbb7510c',
        '_siteStatDay': '20181211',
        '_siteStatRedirectUv': 'redirectUv_17361940',
        '_siteStatVisitorType': 'visitorType_17361940',
        'JSESSIONID': '906E525D49196B58DC69D39D5510C641',
        'uid': 'a4839a86-dcf1-45c8-8bc3-0c1ce6cdf0c1',
        'oid': 'UAGAP00003921',
        'c': 'ede59026-eac6-432d-a715-735e838e7185',
    }

    def parse(self, response):
        # http://api.zqz510.com//tmof/query?ftxt=&ti=&apS=&pdStart=2016-12-31&pdEnd=2016-11-32&ty=&psty=&law=
        # &litem=&pageNum=1&callback=_jqjsp&_1544509290899=
        url = 'http://api.zqz510.com//tmof/query?ftxt=&ti=&apS=&pdStart=&pdEnd=&ty=&psty=&law=&litem=&pageNum=1' \
              '&apS=&apD=&ag=&judgd=&tid=&cid=&callback=_jqjsp&_{}='.format(str(int(time.time() * 1000)))

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
        print(json_text)
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

            yield item
