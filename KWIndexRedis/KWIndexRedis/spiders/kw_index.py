from urllib.parse import quote
import scrapy
import redis

from scrapy_redis.spiders import RedisSpider
from KWIndexRedis.items import KwindexItem
from main import num
# num = '6'

keyword_key = 'keyword_key%s' % num


class KeywordSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'kw_index_%s' % num
    redis_key = 'kw_index:start_urls'
    allowed_domains = ['chinaz.com']
    start_urls = ['http://index.chinaz.com/']

    def __init__(self):
        super(KeywordSpider).__init__()

        self.connect = redis.Redis(host='127.0.0.1', port=6379, db=15)

    def parse(self, response):
        while True:
            kw = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
            print(kw)
            item = KwindexItem()
            keyword = quote('%s' % kw)
            item['kw'] = kw
            url = response.url + '?words=%s' % keyword
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        strong_index = response.xpath('//ul[@class="zs-nodule bor-b1s clearfix"]/li/div/div/strong/text()').extract()
        print(strong_index)
        if len(strong_index) < 8:
            for i in range(8 - len(strong_index)):
                strong_index.append('未收录')
        [item['sum_index'], item['baidu_pc_index'], item['baidu_mb_index'], item['index_360'], item['sougou_pc_index'],
         item['sougou_mb_index'], item['wechat_index'], item['shenma_index']] = strong_index
        span_index = response.xpath('//ul[@class="zs-nodule bor-b1s clearfix"]/li/div/div/span/text()').extract()
        if len(span_index) < 8:
            for i in range(8 - len(span_index)):
                span_index.append('-')
        [item['sum_index_change'], item['baidu_pc_index_change'], item['baidu_mb_index_change'],
         item['index_360_change'], item['sougou_pc_index_change'], item['sougou_mb_index_change'],
         item['wechat_index_change'], item['shenma_index_change']] = span_index

        # sum_index = response.xpath('//li[@class="nod-li"][2]//strong[@class="fz20 tot"]/text()').extract_first()
        # sum_index_change = response.xpath('//li[@class="nod-li"][2]//span[@class="zs-dec"]/text()').extract_first()
        # baidu_pc_index = response.xpath('//ul[@class="zs-nodule bor-b1s clearfix"]/li[@class="nod-li"][3]/div/'
        #                                 'div/strong[@class="fz20 tot"]/text()').extract_first()
        # baidu_pc_index_change = response.xpath('//ul[@class="zs-nodule bor-b1s clearfix"]/li[@class="nod-li"][3]'
        #                                       '/div/div/span[@class="zs-dec"]/text()').extract_first()
        # baidu_mb_index = response.xpath('//li[@class="nod-li"][4]//strong[@class="fz20 tot"]/text()').extract_first()
        # baidu_mb_index_change = response.xpath('//li[@class="nod-li"][4]//span[@class="zs-dec"]/text()').extract_first()
        # index_360 = response.xpath('//li[@class="nod-li"][5]//strong[@class="fz20 tot"]/text()').extract_first()
        # index_360_change = response.xpath('//li[@class="nod-li"][5]//span[@class="zs-dec"]/text()').extract_first()
        # sougou_pc_index = response.xpath('//li[@class="nod-li"][6]//strong[@class="fz20 tot"]/text()').extract_first()
        # sougou_pc_index_change = response.xpath('//li[@class="nod-li"][6]//span[@class="zs-dec"]/text()').extract_first()
        # sougou_mb_index = response.xpath('//li[@class="nod-li"][7]//strong[@class="fz20 tot"]/text()').extract_first()
        # sougou_mb_index_change = response.xpath('//li[@class="nod-li"][7]//span[@class="zs-dec"]/text()').extract_first()
        # wechat_index = response.xpath('//li[@class="nod-li"][8]//strong[@class="fz20 tot"]/text()').extract_first()
        # wechat_index_change = response.xpath('//li[@class="nod-li"][8]//span[@class="zs-dec"]/text()').extract_first()
        # item['sum_index_change'] = sum_index_change
        # item['baidu_pc_index_change'] = baidu_pc_index_change
        # item['baidu_mb_index'] = baidu_mb_index
        # item['baidu_mb_index_change'] = baidu_mb_index_change
        # item['index_360'] = index_360
        # item['index_360_change'] = index_360_change
        # item['sougou_pc_index'] = sougou_pc_index
        # item['sougou_pc_index_change'] = sougou_pc_index_change
        # item['sougou_mb_index'] = sougou_mb_index
        # item['sougou_mb_index_change'] = sougou_mb_index_change
        # item['wechat_index'] = wechat_index
        # item['wechat_index_change'] = wechat_index_change
        print(item)
        yield item
