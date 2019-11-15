# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
# import re
from scrapy import signals
from my_tools.ip_test import *

# from util.db import get_redis_cli
# from util.proxies import Proxies
connect = redis.Redis(host='127.0.0.1', port=6379, db=11)
nums = 0


class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def process_response(self, request, response, spider):
        # 捕获状态码为40x/50x的response
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            # 随意封装，直接返回response，spider代码中根据url==''来处理response
            connect.sadd('fail_url', request.url)
            # response = HtmlResponse(url='')
            response = None
            return response
        # 其他状态码不处理
        return response


class RandMiddleware(object):

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
        request.headers.setdefault('Referer', 'https://news.sogou.com/')
        ip_ls = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
        print(len(ip_ls))
        if len(ip_ls) < 3:
            get_ip()
        ip = random.choice(ip_ls)
        [proxy_host, proxy_port] = re.compile(r'http://(.*?):(\d+)').findall(ip)[0]
        if not test_ip(proxy_host, proxy_port):
            del_ip('http://' + proxy_host + ':' + proxy_port)
        else:
            request.meta['proxy'] = ip
        return None

    def process_response(self, request, response, spider):
        global nums
        # 检测响应结果,出现302说明这个ip被封了,删除更新ip即可
        if response.status == 302 or 301 and "from=%2fweb%3Fquery%3d" in response.url:
            nums += 1
            # # 302 的 url 需要重新抽取更换
            from_url = re.compile(r"from=%2fweb%3Fquery%3d(.*?)").findall(response.url)[0]
            from_url = 'http://www.sogou.com/web?query=' + from_url
            # connect.sadd('fail_url', from_url)
            # # 因为这个还是会发送到 process_request 中取请求,所以直接在那里会进行更新
            del_ip(request.meta['proxy'])
            request.meta['proxy'] = None
            return request.replace(url=from_url, dont_filter=True)
        elif response.status == 302 or 301 and 'from=%2fnews%3Fquery%3d' in response.url:
            nums += 1
            print('redirect_nums == ', nums)
            if nums >= 10:
                spider.crawler.engine.close_spider(spider, 'close, redirect too many!!!')
            from_url = re.compile(r"from=%2fnews%3Fquery%3d(.*)").findall(response.url)[0]
            from_url = 'https://news.sogou.com/news?query=' + from_url
            del_ip(request.meta['proxy'])
            request.meta['proxy'] = None
            return request.replace(url=from_url, dont_filter=True)
        return response


class SearchSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SearchDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
