# -*- coding: utf-8 -*-
import time

import scrapy
import json

from scrapy_redis.spiders import RedisSpider

from EUIPO_REDIS.items import EuipoItem
# from my_tools.pt_demo import get_cookies
# from main import nums

empty_word = 'null'


class IpoSpider(RedisSpider):
    name = 'ipo'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['https://www.baidu.com/']
    redis_key = 'ipo:start_urls'

    def __init__(self):
        super(IpoSpider).__init__()
        self.cookie = get_cookies()

    def parse(self, response):

        first_url = 'https://euipo.europa.eu/copla/ctmsearch/json'

        # all_num = 1866400

        for page in range(int(nums) * 1000, int(nums) * 1000 + 1000):

            data = {
                'start': '%s' % str(int(page * 100)),
                'rows': '100',
                'searchMode': 'basic',
                'criterion_1': 'ApplicationNumber',
                'term_1': '0',
                'operator_1': 'OR',
                'condition_1': 'CONTAINS',
                'criterion_2': 'MarkVerbalElementText',
                'term_2': '0',
                'operator_2': 'OR',
                'condition_2': 'CONTAINS',
                'criterion_3': 'OppositionIdentifier',
                'term_3': '0',
                'operator_3': 'OR',
                'condition_3': 'CONTAINS',
                'sortField': 'ApplicationNumber',
                'sortOrder': 'asc',
            }

            print(str(int(nums * 100)))

            yield scrapy.FormRequest(url=first_url, formdata=data, callback=self.parse_json, cookies=self.cookie, meta={'num': str(int(nums * 100))})

    def parse_json(self, response):

        num = response.meta['num']
        print(num)
        json_text = json.loads(response.text, encoding='utf-8')

        for data in json_text['items']:
            item = EuipoItem()

            item['num'] = num

            if 'representativeid' in data:
                item['representativeid'] = data['representativeid']
            else:
                item['representativeid'] = empty_word

            if 'basis' in data:
                item['basis'] = data['basis']
            else:
                item['basis'] = empty_word


            if 'nice' in data:
                item['nice'] = data['nice']
            else:
                item['nice'] = empty_word

            if 'numberToShow' in data:
                item['numberToShow'] = data['numberToShow']
            else:
                item['numberToShow'] = empty_word

            if 'publisheddate' in data:
                item['publisheddate'] = data['publisheddate']
            else:
                item['publisheddate'] = empty_word

            if 'type' in data:
                item['this_type'] = data['type']
            else:
                item['this_type'] = empty_word

            if 'publishedsection' in data:
                item['publishedsection'] = data['publishedsection']
            else:
                item['publishedsection'] = empty_word

            if 'statusCode' in data:
                item['statusCode'] = data['statusCode']
            else:
                item['statusCode'] = empty_word

            if 'milestone' in data:
                item['milestone'] = data['milestone']
            else:
                item['milestone'] = empty_word

            if 'thumbnailurl' in data:
                item['thumbnailurl'] = data['thumbnailurl']
            else:
                item['thumbnailurl'] = empty_word

            if 'name' in data:
                item['name'] = data['name']
            else:
                item['name'] = empty_word

            if 'commonDescriptor' in data:
                item['commonDescriptor'] = data['commonDescriptor']
            else:
                item['commonDescriptor'] = empty_word

            if 'applicantname' in data:
                item['applicantname'] = data['applicantname']
            else:
                item['applicantname'] = empty_word

            if 'imageurl' in data:
                item['imageurl'] = data['imageurl']
            else:
                item['imageurl'] = empty_word

            if 'designationdate' in data:
                item['designationdate'] = data['designationdate']
            else:
                item['designationdate'] = empty_word

            if 'applicantsreference' in data:
                item['applicantsreference'] = data['applicantsreference']
            else:
                item['applicantsreference'] = empty_word

            if 'publishedurl' in data:
                item['publishedurl'] = data['publishedurl']
            else:
                item['publishedurl'] = empty_word

            if 'registrationdate' in data:
                item['registrationdate'] = data['registrationdate']
            else:
                item['registrationdate'] = empty_word

            if 'status' in data:
                item['status'] = data['status']
            else:
                item['status'] = empty_word

            if 'applicantStatus' in data:
                item['applicantStatus'] = data['applicantStatus']
            else:
                item['applicantStatus'] = empty_word

            if 'fastTrackIndicator' in data:
                item['fastTrackIndicator'] = data['fastTrackIndicator']
            else:
                item['fastTrackIndicator'] = empty_word

            if 'number' in data:
                item['number'] = data['number']
            else:
                item['number'] = empty_word

            if 'publications' in data:
                item['publications'] = data['publications']
            else:
                item['publications'] = empty_word

            if 'filingdate' in data:
                item['filingdate'] = data['filingdate']
            else:
                item['filingdate'] = empty_word

            if 'controller' in data:
                item['controller'] = data['controller']
            else:
                item['controller'] = empty_word

            if 'applicantid' in data:
                item['applicantid'] = data['applicantid']
            else:
                item['applicantid'] = empty_word

            if 'representativename' in data:
                item['representativename'] = data['representativename']
            else:
                item['representativename'] = empty_word

            yield item

        time.sleep(30)
