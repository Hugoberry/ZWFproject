# -*- coding: utf-8 -*-
import scrapy
import json

from EUIPO.items import EuipoItem

empty_word = 'null'


class IpoSpider(scrapy.Spider):
    name = 'ipo'
    allowed_domains = ['euipo.europa.eu']
    start_urls = ['http://euipo.europa.eu/']

    def parse(self, response):

        first_url = 'https://euipo.europa.eu/copla/ctmsearch/json'

        cookie = {
            'JSESSIONID': '430F9B43C55D07655F1C5A1E36922158.copla3',
            'TS0159664b': '010dad8a7aad5b474bc0a8b716a1e5d684f4b48f2b9f42c98f2d0aa7b3211cee3dd56255f4a484412ef4b172c85eccc64bd6a85a3b03c062f6ef32680f7c6277e1a3741dead715dd1f7baa3ef3276a03d5734487e3',
            'TSPD_101': '0831631732ab2800d0366556974779fe928745592a65d4983b521da10a09be07c56a54ea93223ad0638c83e6f14caf43:',
            'TS0160d57f': '010dad8a7a09cf51323da27141edb0e4f4f20693095e85456cbb8ede63886d8b8d7bf0f5c9997664b4e844aa84e2f938c10046d72491c8ac05e73327e281671ecce25cc9db',
            '__utma': '106981910.1726864177.1545636763.1545636763.1545636763.1',
            '__utmc': '106981910',
            '__utmz': '106981910.1545636763.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            '__utmb': '106981910.2.10.1545636763',
            '_pk_id.26.18ee': '179329495b1ec6d2.1545636763.1.1545636763.1545636763.',
            ' _pk_ses.26.18ee': '*',
            'TS01976a55': '010dad8a7a64b022dd34b88673ad94ab2591ca9fbd9f42c98f2d0aa7b3211cee3dd56255f496719ffd490455e35e17c1af9a30bbcf55156b01753f17a97c539f61225fd152',
            'GUEST_LANGUAGE_ID': 'en_GB',
            'COOKIE_SUPPORT': 'true',
            'TS01b54a83': '010dad8a7a0fedad2e2dfeb1de20519ad3d4094ba780182c439011e8ad3ba4240bd591804321e294604da0a906c6b374ec90d674827f2654634c836ca48d954598c977aa53830b444a037ea4b8abdd5aaa1ad7dec9ee5e44ccb1209e19a986ed27705a25a0'
        }

        all_num = 1862113

        for num in range(int(all_num / 100) + 1):

            data = {
                'start': '%s' % str(int(num * 100)),
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

            yield scrapy.FormRequest(url=first_url, formdata=data, callback=self.parse_json, cookies=cookie)

    def parse_json(self, response):
        json_text = json.loads(response.text, encoding='utf-8')

        for data in json_text['items']:
            item = EuipoItem()

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
