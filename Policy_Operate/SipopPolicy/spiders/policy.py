# -*- coding: utf-8 -*-
import scrapy
import time
import json

from SipopPolicy.items import SipoppolicyItem

empty_word = 'null'


class PolicySpider(scrapy.Spider):
    name = 'policy'
    allowed_domains = ['sipop.cn']
    start_urls = ['http://www.sipop.cn/module/gate/homePage.html']

    def parse(self, response):
        first_url = 'http://www.sipop.cn/patent-interface-web/policy/queryListPolicyOneN?appKey=fichinfoPotal' \
                    '&accessToken=POLICY_TOKEN&pageNum=1&pageSize=10&contentAttributeCode=1100%2C1700%2C1800' \
                    '&_={}'.format(str(int(time.time() * 1000)))
        yield scrapy.Request(url=first_url, callback=self.parse_pages)

    def parse_pages(self, response):
        json_text = json.loads(response.text, encoding='utf-8')
        total = int(json_text['data']['total'])
        pages = int(total / 10 + 1)
        # policy_id_ls = json_text['data']['dataList']
        for page in range(pages):
            list_url = 'http://www.sipop.cn/patent-interface-web/policy/queryListPolicyOneN?appKey=' \
                       'fichinfoPotal&accessToken=POLICY_TOKEN&pageNum={}&pageSize=10&contentAttributeCode' \
                       '=1100%2C1700%2C1800&_={}'.format(str(int(page + 1)), str(int(time.time() * 1000)))
            yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        json_text = json.loads(response.text, encoding='utf-8')
        policy_id_ls = json_text['data']['dataList']
        for policy_id_mode in policy_id_ls:
            policy_id = policy_id_mode['policyId']
            detail_url = 'http://www.sipop.cn/patent-interface-web/policy/getPolicyWithPolicyId?appKey=' \
                         'fichinfoPotal&accessToken=POLICY_TOKEN&policyId={}&_={}'.format(str(policy_id), str(int(time.time() * 1000)))
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = SipoppolicyItem()
        json_text = json.loads(response.text, encoding='utf-8')

        # 解析所有的字段
        if 'abandonedDocument' in json_text['data']:
            item['abandonedDocument'] = json_text['data']['abandonedDocument']
        else:
            item['abandonedDocument'] = empty_word

        if 'area' in json_text['data']:
            item['area'] = json_text['data']['area']
        else:
            item['area'] = empty_word

        if 'areaCode' in json_text['data']:
            item['areaCode'] = json_text['data']['areaCode']
        else:
            item['areaCode'] = empty_word

        if 'attachementFileName' in json_text['data']:
            item['attachementFileName'] = json_text['data']['attachementFileName']
        else:
            item['attachementFileName'] = empty_word

        if 'attachementOSSUrl' in json_text['data']:
            item['attachementOSSUrl'] = json_text['data']['attachementOSSUrl']
        else:
            item['attachementOSSUrl'] = empty_word

        if 'attachmentId' in json_text['data']:
            item['attachmentId'] = json_text['data']['attachmentId']
        else:
            item['attachmentId'] = empty_word

        if 'attachmentLocalUrl' in json_text['data']:
            item['attachmentLocalUrl'] = json_text['data']['attachmentLocalUrl']
        else:
            item['attachmentLocalUrl'] = empty_word

        if 'attachmentName' in json_text['data']:
            item['attachmentName'] = json_text['data']['attachmentName']
        else:
            item['attachmentName'] = empty_word

        if 'city' in json_text['data']:
            item['city'] = json_text['data']['city']
        else:
            item['city'] = empty_word

        if 'cityCode' in json_text['data']:
            item['cityCode'] = json_text['data']['cityCode']
        else:
            item['cityCode'] = empty_word

        if 'contentAttribute' in json_text['data']:
            item['contentAttribute'] = json_text['data']['contentAttribute']
        else:
            item['contentAttribute'] = empty_word

        if 'contentAttributeCode' in json_text['data']:
            item['contentAttributeCode'] = json_text['data']['contentAttributeCode']
        else:
            item['contentAttributeCode'] = empty_word

        if 'createUserId' in json_text['data']:
            item['createUserId'] = json_text['data']['createUserId']
        else:
            item['createUserId'] = empty_word

        if 'createUserName' in json_text['data']:
            item['createUserName'] = json_text['data']['createUserName']
        else:
            item['createUserName'] = empty_word

        if 'fileOriginal' in json_text['data']:
            item['fileOriginal'] = json_text['data']['fileOriginal']
        else:
            item['fileOriginal'] = empty_word

        if 'fileRemark' in json_text['data']:
            item['fileRemark'] = json_text['data']['fileRemark']
        else:
            item['fileRemark'] = empty_word

        if 'handleState' in json_text['data']:
            item['handleState'] = json_text['data']['handleState']
        else:
            item['handleState'] = empty_word

        if 'id' in json_text['data']:
            item['sipop_id'] = json_text['data']['id']
        else:
            item['sipop_id'] = empty_word

        if 'implementDept' in json_text['data']:
            item['implementDept'] = json_text['data']['implementDept']
        else:
            item['implementDept'] = empty_word

        if 'implementMode' in json_text['data']:
            item['implementMode'] = json_text['data']['implementMode']
        else:
            item['implementMode'] = empty_word

        if 'implementModeCode' in json_text['data']:
            item['implementModeCode'] = json_text['data']['implementModeCode']
        else:
            item['implementModeCode'] = empty_word

        if 'implementationTime' in json_text['data']:
            item['implementationTime'] = json_text['data']['implementationTime']
        else:
            item['implementationTime'] = empty_word

        if 'industry' in json_text['data']:
            item['industry'] = json_text['data']['industry']
        else:
            item['industry'] = empty_word

        if 'industryCode' in json_text['data']:
            item['industryCode'] = json_text['data']['industryCode']
        else:
            item['industryCode'] = empty_word

        if 'isHaveAttachment' in json_text['data']:
            item['isHaveAttachment'] = json_text['data']['isHaveAttachment']
        else:
            item['isHaveAttachment'] = empty_word

        if 'isHaveGraphic' in json_text['data']:
            item['isHaveGraphic'] = json_text['data']['isHaveGraphic']
        else:
            item['isHaveGraphic'] = empty_word

        if 'isHaveProjectDeclaration' in json_text['data']:
            item['isHaveProjectDeclaration'] = json_text['data']['isHaveProjectDeclaration']
        else:
            item['isHaveProjectDeclaration'] = empty_word

        if 'isHaveUnscramble' in json_text['data']:
            item['isHaveUnscramble'] = json_text['data']['isHaveUnscramble']
        else:
            item['isHaveUnscramble'] = empty_word

        if 'isRefuse' in json_text['data']:
            item['isRefuse'] = json_text['data']['isRefuse']
        else:
            item['isRefuse'] = empty_word

        if 'justiceInterpretPolicyId' in json_text['data']:
            item['justiceInterpretPolicyId'] = json_text['data']['justiceInterpretPolicyId']
        else:
            item['justiceInterpretPolicyId'] = empty_word

        if 'justiceInterpretPolicyName' in json_text['data']:
            item['justiceInterpretPolicyName'] = json_text['data']['justiceInterpretPolicyName']
        else:
            item['justiceInterpretPolicyName'] = empty_word

        if 'lastModifiedTime' in json_text['data']:
            item['lastModifiedTime'] = json_text['data']['lastModifiedTime']
        else:
            item['lastModifiedTime'] = empty_word

        if 'maximumFunding' in json_text['data']:
            item['maximumFunding'] = json_text['data']['maximumFunding']
        else:
            item['maximumFunding'] = empty_word

        if 'organization' in json_text['data']:
            item['organization'] = json_text['data']['organization']
        else:
            item['organization'] = empty_word

        if 'organizationAddress' in json_text['data']:
            item['organizationAddress'] = json_text['data']['organizationAddress']
        else:
            item['organizationAddress'] = empty_word

        if 'organizationTelephone' in json_text['data']:
            item['organizationTelephone'] = json_text['data']['organizationTelephone']
        else:
            item['organizationTelephone'] = empty_word

        if 'originalLastWebSite' in json_text['data']:
            item['originalLastWebSite'] = json_text['data']['originalLastWebSite']
        else:
            item['originalLastWebSite'] = empty_word

        if 'originalWebsite' in json_text['data']:
            item['originalWebsite'] = json_text['data']['originalWebsite']
        else:
            item['originalWebsite'] = empty_word

        if 'policyId' in json_text['data']:
            item['policyId'] = json_text['data']['policyId']
        else:
            item['policyId'] = empty_word

        if 'policyName' in json_text['data']:
            item['policyName'] = json_text['data']['policyName']
        else:
            item['policyName'] = empty_word

        if 'policyType' in json_text['data']:
            item['policyType'] = json_text['data']['policyType']
        else:
            item['policyType'] = empty_word

        if 'policyTypeCode' in json_text['data']:
            item['policyTypeCode'] = json_text['data']['policyTypeCode']
        else:
            item['policyTypeCode'] = empty_word

        if 'policyTypeName' in json_text['data']:
            item['policyTypeName'] = json_text['data']['policyTypeName']
        else:
            item['policyTypeName'] = empty_word

        if 'province' in json_text['data']:
            item['province'] = json_text['data']['province']
        else:
            item['province'] = empty_word

        if 'provinceCode' in json_text['data']:
            item['provinceCode'] = json_text['data']['provinceCode']
        else:
            item['provinceCode'] = empty_word

        if 'publicNumber' in json_text['data']:
            item['publicNumber'] = json_text['data']['publicNumber']
        else:
            item['publicNumber'] = empty_word

        if 'publishTime' in json_text['data']:
            item['publishTime'] = json_text['data']['publishTime']
        else:
            item['publishTime'] = empty_word

        if 'recipients' in json_text['data']:
            item['recipients'] = json_text['data']['recipients']
        else:
            item['recipients'] = empty_word

        if 'recipientsCode' in json_text['data']:
            item['recipientsCode'] = json_text['data']['recipientsCode']
        else:
            item['recipientsCode'] = empty_word

        if 'referenceFileName' in json_text['data']:
            item['referenceFileName'] = json_text['data']['referenceFileName']
        else:
            item['referenceFileName'] = empty_word

        if 'region' in json_text['data']:
            item['region'] = json_text['data']['region']
        else:
            item['region'] = empty_word

        if 'remark' in json_text['data']:
            item['remark'] = json_text['data']['remark']
        else:
            item['remark'] = empty_word

        if 'revisedVersion' in json_text['data']:
            item['revisedVersion'] = json_text['data']['revisedVersion']
        else:
            item['revisedVersion'] = empty_word

        if 'scope' in json_text['data']:
            item['scope'] = json_text['data']['scope']
        else:
            item['scope'] = empty_word

        if 'stage' in json_text['data']:
            item['stage'] = json_text['data']['stage']
        else:
            item['stage'] = empty_word

        if 'technicalField' in json_text['data']:
            item['technicalField'] = json_text['data']['technicalField']
        else:
            item['technicalField'] = empty_word

        if 'validity' in json_text['data']:
            item['validity'] = json_text['data']['validity']
        else:
            item['validity'] = empty_word

        if 'validityCode' in json_text['data']:
            item['validityCode'] = json_text['data']['validityCode']
        else:
            item['validityCode'] = empty_word

        if 'validityDate' in json_text['data']:
            item['validityDate'] = json_text['data']['validityDate']
        else:
            item['validityDate'] = empty_word

        if 'validityName' in json_text['data']:
            item['validityName'] = json_text['data']['validityName']
        else:
            item['validityName'] = empty_word

        if 'yfsj' in json_text['data']:
            item['yfsj'] = json_text['data']['yfsj']
        else:
            item['yfsj'] = empty_word

        yield item
