import json

from scrapy_redis.spiders import RedisSpider
import scrapy
import time

from SipopPolicyImg.items import SipoppolicyItem

empty_word = 'null'


class PolicySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'policy_img'
    redis_key = 'policy_img:start_urls'
    allowed_domains = ['sipop.cn']
    start_urls = ['http://www.sipop.cn/module/gate/policy/policiesDiagramList.html']

    def parse(self, response):
        # http://www.sipop.cn/patent-interface-web/graphic/queryGraphic?appKey=
        # fichinfoPotal&accessToken=POLICY_TOKEN&pageNum=1&pageSize=10&_=1544085922815
        first_url = 'http://www.sipop.cn/patent-interface-web/graphic/queryGraphic?appKey=fichinfoPotal&' \
                    'accessToken=POLICY_TOKEN&pageNum=1&pageSize=10&_={}'.format(str(int(time.time() * 1000)))
        yield scrapy.Request(url=first_url, callback=self.parse_pages)

    def parse_pages(self, response):
        json_text = json.loads(response.text, encoding='utf-8')
        total = int(json_text['data']['total'])
        pages = int(total / 10 + 1)
        # policy_id_ls = json_text['data']['dataList']
        for page in range(pages):
            list_url = 'http://www.sipop.cn/patent-interface-web/graphic/queryGraphic?appKey=fichinfoPotal&' \
                       'accessToken=POLICY_TOKEN&pageNum={}&pageSize=10&_={}'.format(str(int(page + 1)), str(int(time.time() * 1000)))
            yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        json_text = json.loads(response.text, encoding='utf-8')
        for data in json_text['data']['dataList']:
            item = SipoppolicyItem()

            if 'area' in data:
                item['area'] = data['area']
            else:
                item['area'] = empty_word

            if 'areaCode' in data:
                item['areaCode'] = data['areaCode']
            else:
                item['areaCode'] = empty_word

            if 'city' in data:
                item['city'] = data['city']
            else:
                item['city'] = empty_word

            if 'cityCode' in data:
                item['cityCode'] = data['cityCode']
            else:
                item['cityCode'] = empty_word

            if 'graphicId' in data:
                item['graphicId'] = data['graphicId']
            else:
                item['graphicId'] = empty_word

            if 'graphicTitle' in data:
                item['graphicTitle'] = data['graphicTitle']
            else:
                item['graphicTitle'] = empty_word

            if 'graphicType' in data:
                item['graphicType'] = data['graphicType']
            else:
                item['graphicType'] = empty_word

            if 'id' in data:
                item['this_id'] = data['id']
            else:
                item['this_id'] = empty_word

            if 'originalLastWebSite' in data:
                item['originalLastWebSite'] = data['originalLastWebSite']
            else:
                item['originalLastWebSite'] = empty_word

            if 'policyContent' in data:
                item['policyContent'] = data['policyContent']
            else:
                item['policyContent'] = empty_word

            if 'policyContentUrl' in data:
                item['policyContentUrl'] = data['policyContentUrl']
            else:
                item['policyContentUrl'] = empty_word

            if 'policyId' in data:
                item['policyId'] = data['policyId']
            else:
                item['policyId'] = empty_word

            if 'policyOrg' in data:
                item['policyOrg'] = data['policyOrg']
            else:
                item['policyOrg'] = empty_word

            if 'province' in data:
                item['province'] = data['province']
            else:
                item['province'] = empty_word

            if 'provinceCode' in data:
                item['provinceCode'] = data['provinceCode']
            else:
                item['provinceCode'] = empty_word

            if 'publishTime' in data:
                item['publishTime'] = data['publishTime']
            else:
                item['publishTime'] = empty_word

            if 'region' in data:
                item['region'] = data['region']
            else:
                item['region'] = empty_word

            if 'releaseDate' in data:
                item['releaseDate'] = data['releaseDate']
            else:
                item['releaseDate'] = empty_word

            yield item
