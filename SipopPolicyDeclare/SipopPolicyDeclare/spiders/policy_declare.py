import json

from scrapy_redis.spiders import RedisSpider
import scrapy
import time

from SipopPolicyDeclare.items import SipoppolicyItem

empty_word = 'null'


class PolicySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'policy_declare'
    redis_key = 'policy_declare:start_urls'
    allowed_domains = ['sipop.cn']
    start_urls = ['http://www.sipop.cn/module/gate/policy/projectApplicationList.html']

    def parse(self, response):
        # http://www.sipop.cn/patent-interface-web/projectDeclar/queryProjectDeclar?appKey=fichinfoPotal&
        # accessToken=POLICY_TOKEN&pageNum=1&pageSize=10&_=1544144337059
        first_url = 'http://www.sipop.cn/patent-interface-web/projectDeclar/queryProjectDeclar?appKey=fichinfoPotal&' \
                    'accessToken=POLICY_TOKEN&pageNum=1&pageSize=10&_={}'.format(str(int(time.time() * 1000)))
        yield scrapy.Request(url=first_url, callback=self.parse_pages)

    def parse_pages(self, response):
        json_text = json.loads(response.text, encoding='utf-8')
        total = int(json_text['data']['total'])
        pages = int(total / 10 + 1)
        # policy_id_ls = json_text['data']['dataList']
        for page in range(pages):
            list_url = 'http://www.sipop.cn/patent-interface-web/projectDeclar/queryProjectDeclar?appKey=fichinfoPotal&' \
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

            if 'attachmentLocalUrl' in data:
                item['attachmentLocalUrl'] = data['attachmentLocalUrl']
            else:
                item['attachmentLocalUrl'] = empty_word

            if 'attachmentName' in data:
                item['attachmentName'] = data['attachmentName']
            else:
                item['attachmentName'] = empty_word

            if 'city' in data:
                item['city'] = data['city']
            else:
                item['city'] = empty_word

            if 'cityCode' in data:
                item['cityCode'] = data['cityCode']
            else:
                item['cityCode'] = empty_word

            if 'createUserName' in data:
                item['createUserName'] = data['createUserName']
            else:
                item['createUserName'] = empty_word

            if 'declarAcceptOrg' in data:
                item['declarAcceptOrg'] = data['declarAcceptOrg']
            else:
                item['declarAcceptOrg'] = empty_word

            if 'declarAcceptOrgAddress' in data:
                item['declarAcceptOrgAddress'] = data['declarAcceptOrgAddress']
            else:
                item['declarAcceptOrgAddress'] = empty_word

            if 'declarAcceptTelephone' in data:
                item['declarAcceptTelephone'] = data['declarAcceptTelephone']
            else:
                item['declarAcceptTelephone'] = empty_word

            if 'declarBeginTime' in data:
                item['declarBeginTime'] = data['declarBeginTime']
            else:
                item['declarBeginTime'] = empty_word

            if 'declarConsultMail' in data:
                item['declarConsultMail'] = data['declarConsultMail']
            else:
                item['declarConsultMail'] = empty_word

            if 'declarContent' in data:
                item['declarContent'] = data['declarContent']
            else:
                item['declarContent'] = empty_word

            if 'declarContentKeyWord' in data:
                item['declarContentKeyWord'] = data['declarContentKeyWord']
            else:
                item['declarContentKeyWord'] = empty_word

            if 'declarDispatchTime' in data:
                item['declarDispatchTime'] = data['declarDispatchTime']
            else:
                item['declarDispatchTime'] = empty_word

            if 'declarEndTime' in data:
                item['declarEndTime'] = data['declarEndTime']
            else:
                item['declarEndTime'] = empty_word

            if 'declarMail' in data:
                item['declarMail'] = data['declarMail']
            else:
                item['declarMail'] = empty_word

            if 'declarObject' in data:
                item['declarObject'] = data['declarObject']
            else:
                item['declarObject'] = empty_word

            if 'declarOrgZipcode' in data:
                item['declarOrgZipcode'] = data['declarOrgZipcode']
            else:
                item['declarOrgZipcode'] = empty_word

            if 'declarRequire' in data:
                item['declarRequire'] = data['declarRequire']
            else:
                item['declarRequire'] = empty_word

            if 'declarTopicName' in data:
                item['declarTopicName'] = data['declarTopicName']
            else:
                item['declarTopicName'] = empty_word

            if 'declarUrl' in data:
                item['declarUrl'] = data['declarUrl']
            else:
                item['declarUrl'] = empty_word

            if 'handleState' in data:
                item['handleState'] = data['handleState']
            else:
                item['handleState'] = empty_word

            if 'id' in data:
                item['this_id'] = data['id']
            else:
                item['this_id'] = empty_word

            if 'isHaveAttachment' in data:
                item['isHaveAttachment'] = data['isHaveAttachment']
            else:
                item['isHaveAttachment'] = empty_word

            if 'isRefuse' in data:
                item['isRefuse'] = data['isRefuse']
            else:
                item['isRefuse'] = empty_word

            if 'orgAddress' in data:
                item['orgAddress'] = data['orgAddress']
            else:
                item['orgAddress'] = empty_word

            if 'orgTelephone' in data:
                item['orgTelephone'] = data['orgTelephone']
            else:
                item['orgTelephone'] = empty_word

            if 'organization' in data:
                item['organization'] = data['organization']
            else:
                item['organization'] = empty_word

            if 'originalLastWebSite' in data:
                item['originalLastWebSite'] = data['originalLastWebSite']
            else:
                item['originalLastWebSite'] = empty_word

            if 'policyId' in data:
                item['policyId'] = data['policyId']
            else:
                item['policyId'] = empty_word

            if 'policyIds' in data:
                item['policyIds'] = data['policyIds']
            else:
                item['policyIds'] = empty_word

            if 'policyNames' in data:
                item['policyNames'] = data['policyNames']
            else:
                item['policyNames'] = empty_word

            if 'projectDeclarType' in data:
                item['projectDeclarType'] = data['projectDeclarType']
            else:
                item['projectDeclarType'] = empty_word

            if 'projectId' in data:
                item['projectId'] = data['projectId']
            else:
                item['projectId'] = empty_word

            if 'projectName' in data:
                item['projectName'] = data['projectName']
            else:
                item['projectName'] = empty_word

            if 'province' in data:
                item['province'] = data['province']
            else:
                item['province'] = empty_word

            if 'provinceCode' in data:
                item['provinceCode'] = data['provinceCode']
            else:
                item['provinceCode'] = empty_word

            if 'region' in data:
                item['region'] = data['region']
            else:
                item['region'] = empty_word

            if 'releaseDate' in data:
                item['releaseDate'] = data['releaseDate']
            else:
                item['releaseDate'] = empty_word

            if 'remark' in data:
                item['remark'] = data['remark']
            else:
                item['remark'] = empty_word

            yield item
