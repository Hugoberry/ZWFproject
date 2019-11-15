# -*- coding: utf-8 -*-
import redis

import scrapy
import json

from scrapy.spidermiddlewares.httperror import HttpError, logger
from scrapy_redis.spiders import RedisSpider
from twisted.internet.error import TCPTimedOutError, DNSLookupError

from main import num
from my_tools.pt_demo import IPCookie

from EUIPO_REDIS.items import DocumentItem
# from my_tools.pt_demo import get_cookies

empty_word = 'null'
keyword_key = 'keyword_key'
ip_cookie_key = 'ip_cookie_key_%s' % num


class IpoSpider(RedisSpider):
    name = 'ipo_document'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['https://www.baidu.com/']
    redis_key = 'ipo:start_urls'

    def __init__(self):
        super(IpoSpider).__init__()
        # 这个编号是对 parse_documents 函数实现回调用的
        self.documents_page = 1
        self.connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
        try:
            self.cookie = json.loads(list(eval(self.connect.lindex(ip_cookie_key, 0).decode('utf-8')))[1])
        except Exception as e:
            print(e)
            IPCookie().get_cookies()
            self.cookie = json.loads(list(eval(self.connect.lindex(ip_cookie_key, 0).decode('utf-8')))[1])

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            while True:
                self.connect.blpop(ip_cookie_key, 1)
                if self.connect.llen(ip_cookie_key) == 0:
                    break
            IPCookie().get_cookies()

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            while True:
                self.connect.blpop(ip_cookie_key, 1)
                if self.connect.llen(ip_cookie_key) == 0:
                    break
            IPCookie().get_cookies()

            response = failure.response
            logger.error('HttpError on %s', response.url)

    def parse(self, response):

        try:

            while True:
                nums = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                print(nums)
                first_url = 'https://euipo.europa.eu/copla/trademark/data/withDocuments/%s?sEcho=1&iColumns=7&sColumns=&iDisplayStart=0&iDisplayLength=10&mDataProp_0=function&mDataProp_1=function&mDataProp_2=function&mDataProp_3=function&mDataProp_4=function&mDataProp_5=function&mDataProp_6=function&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&iSortingCols=1&iSortCol_0=5&sSortDir_0=desc&bSortable_0=false&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=false' % nums

                yield scrapy.Request(url=first_url, callback=self.parse_document, cookies=self.cookie, meta={'nums': nums}, errback=self.errback_twisted)

        except TypeError:
            pass

    def parse_document(self, response):
        item = DocumentItem()

        nums = response.meta['nums']
        print(nums)
        json_text = json.loads(response.text, encoding='utf-8')

        item['nums'] = nums
        item['aaData'] = str(json_text['aaData'])
        item['iTotalDisplayRecords'] = str(json_text['iTotalDisplayRecords'])
        item['iTotalRecords'] = str(json_text['iTotalRecords'])
        item['sEcho'] = str(json_text['sEcho'])

        yield item

        all_pages = (int(json_text['iTotalRecords']) / 10) + 1

        if all_pages > 2:
            for page in range(int(all_pages) - 1):
                self.documents_page += 1
                documents_url = 'https://euipo.europa.eu/copla/trademark/data/withDocuments/000000001?sEcho=%s&iColumns=7&sColumns=&iDisplayStart=0&iDisplayLength=10&mDataProp_0=function&mDataProp_1=function&mDataProp_2=function&mDataProp_3=function&mDataProp_4=function&mDataProp_5=function&mDataProp_6=function&sSearch=&bRegex=false&sSearch_0=&bRegex_0=false&bSearchable_0=true&sSearch_1=&bRegex_1=false&bSearchable_1=true&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch_3=&bRegex_3=false&bSearchable_3=true&sSearch_4=&bRegex_4=false&bSearchable_4=true&sSearch_5=&bRegex_5=false&bSearchable_5=true&sSearch_6=&bRegex_6=false&bSearchable_6=true&iSortingCols=1&iSortCol_0=5&sSortDir_0=desc&bSortable_0=false&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&bSortable_5=true&bSortable_6=false' % str(self.documents_page)
                yield scrapy.Request(url=documents_url, callback=self.parse_again, cookies=self.cookie, meta={'nums': nums}, errback=self.errback_twisted)

    def parse_again(self, response):
        item = DocumentItem()

        nums = response.meta['nums']
        print(nums)
        json_text = json.loads(response.text, encoding='utf-8')

        item['nums'] = nums
        item['aaData'] = str(json_text['aaData'])
        item['iTotalDisplayRecords'] = str(json_text['iTotalDisplayRecords'])
        item['iTotalRecords'] = str(json_text['iTotalRecords'])
        item['sEcho'] = str(json_text['sEcho'])

        yield item
