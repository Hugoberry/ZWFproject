import redis
import scrapy
from scrapy_redis.spiders import RedisSpider
import re
from scrapy.spidermiddlewares.httperror import HttpError, logger
from twisted.internet.error import *

from Url_Confirm_Redis.items import UrlConfirmItem

empty_word = 'null'
connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
keyword_key = 'keyword_key'
fail_url = 'fail_url'


class UrlDemoSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'url_confirm_redis'
    redis_key = 'url_confirm:start_urls'
    allowed_domains = ['chinaz.com']
    start_urls = ['http://icp.chinaz.com/']

    def errback_twisted(self, failure):
        if failure.check(TimeoutError, TCPTimedOutError, DNSLookupError):
            request = failure.request
            connect.sadd(fail_url, request.url)
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            request = failure.value.request
            connect.sadd(fail_url, request.url)
            logger.error('HttpError on %s', response.url)

    def parse(self, response):
        for x in range(connect.llen(keyword_key)):
            info = connect.lindex(keyword_key, 0).decode('utf-8').strip()
            connect.lrem(keyword_key, info)
            print(info)
            info = re.compile(r'(.*)\t(.*)').findall(info)[0]
            kw = info[0]
            test_url = info[1]
            item = UrlConfirmItem()
            item['kw'] = kw
            item['domain'] = test_url
            new_url = response.url + test_url
            yield scrapy.Request(url=new_url, callback=self.parse_detail, method='post', meta={'item': item},
                                 dont_filter=True)

    def parse_detail(self, response):
        text = response.text
        item = response.meta['item']

        if not re.compile(r'<p id="err" class="tc col-red fz18 YaHei pb20">未备案或者备案取消，获取最新数据请<a href'
                          r'="javascript:" class="updateByVcode">\((.*?)\)</a></p>').findall(text):

            # 这里[0]取不到
            if re.compile(r'以下信息更新时间：(.*?)</span>').findall(text):
                item['update_time'] = re.compile(r'以下信息更新时间：(.*?)</span>').findall(text)[0]
            else:
                item['update_time'] = empty_word
            # 这里也没有
            if re.compile(r'<span>主办单位名称</span><p>(.*?)<a class="fz12 pl5"').findall(text):
                item['company_name'] = re.compile(r'<span>主办单位名称</span><p>(.*?)<a class="fz12 pl5"').findall(text)[0]
            else:
                item['company_name'] = empty_word
            if re.compile(r'<strong class="fl fwnone">(.*?)</strong>').findall(text):
                item['company_type'] = re.compile(r'<strong class="fl fwnone">(.*?)</strong>').findall(text)[0]
            else:
                item['company_type'] = empty_word

            if re.compile(r'<p class="fz18 col-blue02 YaHei bg-white ptb10 pl15">(.*?)</p>').findall(text) == [
                '该单位还备案了以下网站']:
                ajax_url = 'http://icp.chinaz.com/ajaxsync.aspx?at=beiansl&host={}&type=host'.format(item['domain'])
                yield scrapy.Request(url=ajax_url, callback=self.parse_ajax, meta={'item': item}, dont_filter=True)
            else:
                item['company_no'] = re.compile(r'<span>网站备案/许可证号</span><p><font>(.*?)</font>').findall(text)[0]
                item['company_web_name'] = re.compile(r'<span>网站名称</span><p>(.*?)</p></li>').findall(text)[0]
                item['company_url'] = re.compile(r'<span>网站首页网址</span><p class="Wzno">(.*?)</p></li>').findall(text)[0]
                item['check_time'] = re.compile(r'<span>审核时间</span><p>(.*?)</p></li>').findall(text)[0]
                yield item
        else:
            item['update_time'] = empty_word
            item['company_name'] = empty_word
            item['company_type'] = empty_word
            item['company_no'] = empty_word
            item['company_web_name'] = empty_word
            item['company_url'] = empty_word
            item['check_time'] = empty_word
            yield item

    def parse_ajax(self, response):
        item = response.meta['item']
        aim = response.text[1:-1].split('{results:')[1][:-1][1:-1]
        aim_ls = re.compile(r'{(.*?)}').findall(aim)
        if not aim_ls:
            item['company_no'] = empty_word
            item['company_web_name'] = empty_word
            item['company_url'] = empty_word
            item['check_time'] = empty_word
            yield item
        else:
            for result in aim_ls:
                item['company_no'] = re.compile(r'SiteLicense:"(.*?)"').findall(result)[0]
                item['company_web_name'] = re.compile(r'SiteName:"(.*?)"').findall(result)[0]
                item['company_url'] = re.compile(r'MainPage:"(.*?)"').findall(result)[0]
                item['check_time'] = re.compile(r'VerifyTime:"(.*?)"').findall(result)[0]
                yield item
