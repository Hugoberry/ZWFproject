# -*- coding: utf-8 -*-
import re
import json
import random
import time
from urllib.parse import quote, unquote
import scrapy
from ZhihuLive.items import ZhihuliveItem

empty_word = 'null'


class ZhLiveSpider(scrapy.Spider):
    name = 'zh_live'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        file = open(r'./a.txt', 'r+')
        line = file.readlines()
        len_len = len(line)
        for word in range(len_len):
            kw = line[word].replace('(', '').replace(',1)', '').strip()
            print(kw)
            new_url = 'https://www.zhihu.com/search?type=live&q=%s' % quote(kw)
            item = ZhihuliveItem()
            item['kw'] = kw
            time.sleep(random.random())
            yield scrapy.Request(url=new_url, callback=self.parse_raw, meta={'item': item})

    def parse_raw(self, response):
        kw = response.meta['item']['kw']
        text = response.text
        search_hash_id = re.compile(r'"searchHashId":"(.*?)"}}').findall(text)[0]
        print(search_hash_id)
        search_hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=live&q={}&correction=1&offset=5&limit=10' \
                          '&show_all_topics=0&search_hash_id={}'.format(quote(kw), search_hash_id)
        info = response.xpath('//div[@class="List"]/div[1]/div[@class="List-item"]')
        if not info:
            item = response.meta['item']
            item['title'] = empty_word
            item['description'] = empty_word
            item['speakers_name'] = empty_word
            item['target_url'] = empty_word
            item['estimation'] = empty_word
            item['zh_id'] = empty_word
        else:
            for i in info:
                item = response.meta['item']
                kw = item['kw']
                title = i.xpath('./div[@class="ContentItem"]//div[@class="ContentItem-head"]/h2[@class'
                                '="ContentItem-title"]//span/text()').extract_first()
                description = i.xpath('./div[@class="ContentItem"]//div[@class="RichText ztext SearchItem-'
                                      'description Highlight"]').extract_first()
                description = re.compile(r'<div class="RichText ztext SearchItem-description Highlight">(.*?)</div>'
                                         ).findall(description)[0]
                speakers_name = i.xpath('./div[@class="ContentItem"]//span[@class="Search-liveStatusLink"]/span'
                                        '//span/text()').extract_first()
                speakers_name = ''.join(speakers_name)
                target_url = i.xpath('./div[@class="ContentItem"]//h2[@class="ContentItem-title"]/div/a/@href'
                                     ).extract_first()
                taken = i.xpath('./div[@class="ContentItem"]//span[@class="Search-liveStatusLink"][3]/text()[1]'
                                ).extract_first()
                estimation = i.xpath('./div[@class="ContentItem"]//span[@class="Search-liveStatusLink"][2]//'
                                     'svg/@class').extract()
                estimation = str(estimation.count('Icon Icon--rating') + estimation.count('Icon Icon--ratingHalf') * .5)
                print(estimation)
                item['title'] = title if title else empty_word
                item['description'] = description if description else empty_word
                item['speakers_name'] = speakers_name if speakers_name else empty_word
                item['target_url'] = target_url if target_url else empty_word
                item['estimation'] = str(estimation) if estimation else empty_word
                item['taken'] = taken if taken else empty_word
                item['zh_id'] = str(info.index(i) + 1)
                if item['zh_id'] == '5':
                    yield item
                    yield scrapy.Request(url=search_hash_url, callback=self.parse_ajax, meta={'kw': kw})
                else:
                    yield item

    def parse_ajax(self, response):
        kw = unquote(re.compile('q=(.*?)&').findall(response.url)[0])
        # https://www.zhihu.com/api/v4/search_v3?t=live&q=%E8%8B%B1%E9%9B%84%E8%81%94%E7%9B%9F&correction=1&
        # offset=5&limit=10&show_all_topics=0&search_hash_id=3185123e20fb44646c91ba969fa40a15
        # https://www.zhihu.com/api/v4/search_v3?t=live&q=%E8%8B%B1%E9%9B%84%E8%81%94%E7%9B%9F&correction=1&
        # offset=5&limit=10&show_all_topics=0&search_hash_id=356982194b5b773720d0f0f152775e2d
        # (offset, search_hash_id) = re.compile(r'&offset=(\d+)&limit=10&show_all_topics=0&search_hash_id=(.*)'
        #                                       ).findall(response.url)[0]
        # if int(offset) <= 35:
        #     offset = str(int(int(offset) + 10))
        # else:
        #     pass
        # new_hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=live&q={}&correction=1&offset={}&limit=10&' \
        #                'show_all_topics=0&search_hash_id={}'.format(quote(kw), offset, search_hash_id)
        print(json.loads(response.text))
        result = json.loads(response.text)
        if result['paging']['is_end'] == 'false' or 'False':
            next_url = result['paging']['next']
            new_url_ele = re.compile(r'&search_hash_id=(.*?)&q=(.*?)&limit=10&t=live&offset=(\d+)&topic_filter=0'
                                     ).findall(next_url)[0]
            new_hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=live&q={}&correction=1&offset={}&limit=10&' \
                           'show_all_topics=0&search_hash_id={}'.format(new_url_ele[1], new_url_ele[2], new_url_ele[0])
            yield scrapy.Request(url=new_hash_url, callback=self.parse_ajax)

        try:
            for res in result['data']:
                item = ZhihuliveItem()
                item['kw'] = kw
                item['title'] = res['highlight']['title'] if res['highlight']['title'] else empty_word
                item['description'] = res['highlight']['description'] if res['highlight'][
                    'description'] else empty_word
                item['zh_id'] = res['id'] if res['id'] else empty_word
                # item['avatar_url'] = res['speakers'][0]['avatar_url'] if res['speakers'][0]['avatar_url']\
                #     else empty_word
                item['speakers_name'] = res['object']['speakers'][0]['name'] if res['object']['speakers'][0]['name'] else empty_word
                item['target_url'] = res['object']['target_url'] if res['object']['target_url'] else empty_word
                if 'estimation' in res['object']:
                    item['estimation'] = res['object']['estimation'] if res['object']['estimation'] else empty_word
                else:
                    item['estimation'] = empty_word
                item['taken'] = res['object']['seats']['taken'] if res['object']['seats']['taken'] else empty_word
                yield item
        except TypeError:
            print(kw + '----finished!!!')
        else:
            print('%s has been spider!!!' % kw)
            yield None
