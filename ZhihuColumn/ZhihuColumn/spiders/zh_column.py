# -*- coding: utf-8 -*-
import re
import json
import random
import time
import scrapy
from urllib.parse import quote, unquote
from ZhihuColumn.items import ZhihucolumnItem

empty_word = 'null'


class ZhColumnSpider(scrapy.Spider):
    name = 'zh_column'
    allowed_domains = ['zhihu.com', 'baidu.com']
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        file = open(r'./a.txt', 'r+')
        line = file.readlines()
        len_len = len(line)
        for word in range(len_len):
            kw = line[word].replace('(', '').replace(',1)', '').strip()
            print(kw)
            new_url = 'https://www.zhihu.com/search?q=%s&type=column' % quote(kw)
            item = ZhihucolumnItem()
            item['kw'] = kw
            time.sleep(random.random() * 2)
            yield scrapy.Request(url=new_url, callback=self.parse_init_page, meta={'item': item})

    def parse_init_page(self, response):
        kw = response.meta['item']['kw']
        text = response.text
        search_hash_id = re.compile(r'search_hash_id=(.*?)&show_all_topics=').findall(text)[0]
        print(search_hash_id)
        hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=column&q={}&correction=1&' \
                   'offset=5&limit=10&show_all_topics=0&search_hash_id='.format(quote(kw)) + search_hash_id
        par = re.compile('<img class="Avatar Avatar--large" width="60" height="60" src="(.*?)" srcSet="(.*?) 2x" alt="(.*?)"/>'
                 '</div></div></a></div><div class="ContentItem-head"><h2 class="ContentItem-title"><div><a class='
                 '"ColumnLink" href="(.*?)" target="_blank"><div class="Popover"><div id="null-toggle" aria-haspopup='
                 '"true" aria-expanded="false" aria-owns="null-content"><span class="Highlight">(.*?)</span></div>'
                 '</div></a></div></h2><div class="ContentItem-meta"><div><div class="RichText ztext SearchItem-meta '
                 'Highlight">(.*?)</div><div class="ContentItem-status"><span class="ContentItem-statusItem '
                 'Search-statusLink">创建者：<span class="UserLink"><div class="Popover"><div id="null-toggle" '
                 'aria-haspopup="true" aria-expanded="false" aria-owns="null-content"><a class="UserLink-link" '
                 'data-za-detail-view-element_name="User" target="_blank" href="(.*?)">(.*?)</a></div></div></span>'
                 '</span><a class="ContentItem-statusItem Search-statusLink" target="_blank" href="(.*?)">(.*?) 关注'
                 '</a><a class="ContentItem-statusItem Search-statusLink" target="_blank" href="(.*?)">(.*?) 文章</a>')
        info = par.findall(text)
        if not info:
            item = response.meta['item']
            item['title'] = empty_word
            item['description'] = empty_word
            item['id_no'] = empty_word
            item['articles_count'] = empty_word
            item['followers'] = empty_word
            item['avatar_url'] = empty_word
            item['creator_name'] = empty_word
            item['creator_url'] = empty_word
            yield item
        else:
            for i in info:
                item = response.meta['item']
                kw = item['kw']
                item['title'] = i[3] if i[3] else empty_word
                item['description'] = i[5] if i[5] else empty_word
                item['id_no'] = str(info.index(i) + 1)
                item['articles_count'] = i[11] if i[11] else empty_word
                item['followers'] = i[9] if i[9] else empty_word
                item['avatar_url'] = i[1] if i[1] else empty_word
                if '</a>' in i[7]:
                    item['creator_name'] = re.compile(r'(.*?)</a>').findall(i[7])[0]
                else:
                    item['creator_name'] = i[7] if i[7] else empty_word
                item['creator_url'] = i[6] if i[6] else empty_word
                if item['id_no'] == '5':
                    yield item
                    yield scrapy.Request(url=hash_url, callback=self.parse_ajax, meta={'kw': kw})
                else:
                    yield item

    def parse_ajax(self, response):
        kw = unquote(re.compile('q=(.*?)&').findall(response.url)[0])
        hash_url = response.url
        # page = int((int(re.compile('offset=(.*?)&limit=10').findall(hash_url)[0]) - 5) / 10)
        # hash_url = hash_url.replace(str(page), '%s' % str(int(5 + (page + 1) * 10)))
        # hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=column&q=%E5%B0%8F%E7%B1%B3&correction=1&' \
        #            'offset={}&limit=10&show_all_topics=0&search_hash_id='.format(str(5 + init_i * 10)) + hash_id
        print(hash_url)
        print(json.loads(response.text))
        result = json.loads(response.text)
        try:
            if result['paging']['is_end'] == 'false' or 'False':
                for res in result['data']:
                    item = ZhihucolumnItem()
                    item['kw'] = kw
                    item['title'] = res['highlight']['title'] if res['highlight']['title'] else empty_word
                    item['description'] = res['highlight']['description'] if res['highlight']['description'] else empty_word
                    item['id_no'] = res['object']['id'] if res['object']['id'] else empty_word
                    item['articles_count'] = res['object']['articles_count'] if res['object']['articles_count'] else empty_word
                    item['followers'] = res['object']['followers'] if res['object']['followers'] else empty_word
                    item['avatar_url'] = res['object']['avatar_url'] if res['object']['avatar_url'] else empty_word
                    item['creator_name'] = res['object']['author']['name'] if res['object']['author']['name'] else empty_word
                    item['creator_url'] = res['object']['author']['url_token'] if res['object']['author']['url_token'] else empty_word
                    yield item
                yield scrapy.Request(url=result['paging']['next'], callback=self.parse_ajax)
        except TypeError:
            print(kw + '----finished!!!')
        else:
            # item = ZhihucolumnItem()
            # item['kw'] = kw
            # item['title'] = empty_word
            # item['description'] = empty_word
            # item['id_no'] = empty_word
            # item['articles_count'] = empty_word
            # item['followers'] = empty_word
            # item['avatar_url'] = empty_word
            # item['creator_name'] = empty_word
            # item['creator_url'] = empty_word
            # yield item
            pass
