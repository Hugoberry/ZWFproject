# -*- coding: utf-8 -*-
import re
from xpinyin import Pinyin
from scrapy.spidermiddlewares.httperror import HttpError, logger
from twisted.internet.error import *
import scrapy
from DomainTest.items import DomaintestItem
import redis

connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
keyword_key = 'keyword_key'
fail_url = 'fail_url'


class ComDemoSpider(scrapy.Spider):
    name = 'com_demo'
    allowed_domains = ['net.cn']
    start_urls = ['http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=quandashi.com']

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            connect.sadd(fail_url, request.url)
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.response
            request = failure.request
            connect.sadd(fail_url, request.url)
            logger.error('HttpError on %s', response.url)

    def parse(self, response):
        for x in range(connect.llen(keyword_key)):
            kw = connect.lindex(keyword_key, 0).decode('utf-8').strip()
            connect.lrem(keyword_key, kw)
            print(kw)
            item = DomaintestItem()
            item['kw'] = kw
            kw_pinyin = Pinyin().get_pinyin(kw).replace('-', '').replace(' ', '').replace('.', '').lower()
            domain_type_ls = ['com', 'cn', 'net', 'club', 'top', 'xyz', 'vip', 'cc', 'art', 'wang', 'ltd', 'org',
                              'site', 'company', 'email', 'online', 'store', 'live', '公司', '中国', 'info',
                              'mobi', 'co', 'auto', 'shop', '集团', '网址', 'com.cn', 'biz', 'work', 'show',
                              'team', 'world', 'ink', 'run', 'beer', 'cool', 'fund', 'guru', 'plus', 'zone',
                              'today', '信息', '网络', 'center', 'chat', '在线', '中文网', 'city', 'net.cn',
                              'org.cn', 'ren', 'tech', 'wiki', '我爱你', 'fun', 'pro', 'pub', 'red', 'gold',
                              'link', 'ac.cn', 'ah.cn', 'bj.cn', 'cq.cn', 'fj.cn', 'gd.cn', 'group', 'gs.cn',
                              'gx.cn', 'gz.cn', 'ha.cn', 'hb.cn', 'he.cn', 'hi.cn', 'hk.cn', 'hl.cn', 'hn.cn',
                              'jl.cn', 'js.cn', 'jx.cn', 'ln.cn', 'mo.cn', 'nm.cn', 'nx.cn', 'qh.cn', 'sc.cn',
                              'sd.cn', 'sh.cn', 'sn.cn', 'sx.cn', 'tj.cn', 'tw.cn', 'video', 'xj.cn', 'xz.cn',
                              'yn.cn', 'zj.cn', 'design', 'social', '企业', '商店', '游戏', '娱乐']
            for domain_tp in domain_type_ls:
                aim_url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=' + kw_pinyin + '.' + domain_tp
                yield scrapy.Request(url=aim_url, callback=self.parse_detail, meta={'item': item}, errback=self.errback_twisted)

    def parse_detail(self, response):
        item = response.meta['item']
        item['domain_url'] = re.compile('<key>(.*)</key>').findall(response.text)[0]
        item['domain_type'] = re.compile(r'.*?\.(.*)').findall(item['domain_url'])[0]
        item['domain_status'] = re.compile('<original>(.*)</original>').findall(response.text)[0]
        yield item
