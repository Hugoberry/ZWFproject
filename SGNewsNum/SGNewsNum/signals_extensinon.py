from scrapy import signals

nums = 0


class ControlExtension(object):

    def __init__(self, crawler):
        self.crawler = crawler
        crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)

    # crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def item_scraped(self, response, item, spider):
        global nums
        if 'antispider' in response.url:
            nums += 1
        print('redirect_nums == ', nums)
        if nums >= 30:
            self.crawler.engine.close_spider(spider, 'Redirect nums too much, we need close it and restart!!!')
        # if spider.server.exists("close"):
        #     self.crawler.engine.close_spider(spider, '！！！没有 IP 了！！！')
        # if not spider.server.llen(spider.company_queue):
        #     if not spider.server.exists("baidu_spider:requests"):
        #         spider.server.delete(spider.server.proxies.proxies_key)
        #         self.crawler.engine.close_spider(spider, '！！！任务队列完成！！！')
