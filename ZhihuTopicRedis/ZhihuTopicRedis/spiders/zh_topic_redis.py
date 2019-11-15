import re
import json
import random
import time
import scrapy
from urllib.parse import quote, unquote
from ZhihuTopicRedis.items import ZhihutopicItem

empty_word = 'null'
from scrapy_redis.spiders import RedisSpider


class ZhTopicSpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'zh_topic_redis'
    redis_key = 'zh_topic_redis:start_urls'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        file = open(r'./a.txt', 'r+')
        line = file.readlines()
        len_len = len(line)
        for word in range(len_len):
            kw = line[word].replace('(', '').replace(',1)', '').strip()
            print(kw)
            new_url = 'https://www.zhihu.com/search?q=%s&type=topic' % quote(kw)
            item = ZhihutopicItem()
            item['kw'] = kw
            time.sleep(random.random() * 2)
            yield scrapy.Request(url=new_url, callback=self.parse_init_page, meta={'item': item})

    def parse_init_page(self, response):
        kw = response.meta['item']['kw']
        text = response.text
        search_hash_id = re.compile(r'search_hash_id=(.*?)&show_all_topics=').findall(text)[0]
        print(search_hash_id)
        # 'https://www.zhihu.com/api/v4/search_v3?t=topic&q=%E5%B0%8F%E7%B1%B3&correction=1&offset=15&limit=10' \
        # '&show_all_topics=1&search_hash_id=c31acec5d05278b1e09675b63bace886'
        hash_url = 'https://www.zhihu.com/api/v4/search_v3?t=topic&q={}&correction=1&' \
                   'offset=5&limit=10&show_all_topics=1&search_hash_id='.format(quote(kw)) + search_hash_id
        par = re.compile(
            '<div class="List-item"><div class="ContentItem"><div class="ContentItem-main"><div class="'
            'ContentItem-image"><a class="TopicLink" href="(.*?)" target="_blank">'
            '<div class="Popover"><div id="null-toggle" aria-haspopup="true" aria-expanded="false" aria-owns='
            '"null-content"><img class="Avatar Avatar--large TopicLink-avatar" width="60" height="60" src="'
            '(.*?)" srcSet="(.*?) 2x" alt="(.*?)/></div></div></a></div><div class="ContentItem-head">'
            '<h2 class="ContentItem-title"><div><a class="TopicLink" href="(.*?)" target="_blank"><div '
            'class="Popover"><div id="null-toggle" aria-haspopup="true" aria-expanded="false"'
            ' aria-owns="null-content"><span class="Highlight">(.*?)</span></div></div></a></div>'
            '</h2><div class="ContentItem-meta"><div><div class="RichText ztext SearchItem-meta Highlight">'
            '(.*?)</div><div class="ContentItem-status"><a class="ContentItem-statusItem Search-statusLink" '
            'target="_blank" href="(.*?)">(.*?) 关注</a><a class="ContentItem-statusItem'
            ' Search-statusLink" target="_blank" href="(.*?)">(.*?) 问题</a><a class='
            '"ContentItem-statusItem Search-statusLink" target="_blank" href="(.*?)">'
            '(.*?) 精华内容</a>')
        info = par.findall(text)
        if not info:
            item = response.meta['item']
            item['title'] = empty_word
            item['avatar_url'] = empty_word
            item['description'] = empty_word
            item['followers_count'] = empty_word
            item['id_no'] = empty_word
            item['questions_count'] = empty_word
            item['top_answer_count'] = empty_word
            item['topic_url'] = empty_word
            yield item
        else:
            for i in info:
                item = response.meta['item']
                kw = item['kw']
                item['title'] = i[3] if i[3] else empty_word
                item['avatar_url'] = i[2] if i[2] else empty_word
                item['description'] = i[6] if i[6] else empty_word
                item['followers_count'] = i[8] if i[8] else empty_word
                item['id_no'] = str(info.index(i) + 1)
                item['questions_count'] = i[10] if i[10] else empty_word
                item['top_answer_count'] = i[12] if i[12] else empty_word
                item['topic_url'] = i[1] if i[1] else empty_word
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
                    item = ZhihutopicItem()
                    item['kw'] = kw
                    item['title'] = res['highlight']['title'] if res['highlight']['title'] else empty_word
                    item['description'] = res['highlight']['description'] if res['highlight'][
                        'description'] else empty_word
                    item['id_no'] = res['object']['id'] if res['object']['id'] else empty_word
                    item['followers_count'] = res['object']['followers_count'] if res['object'][
                        'followers_count'] else empty_word
                    item['questions_count'] = res['object']['questions_count'] if res['object'][
                        'questions_count'] else empty_word
                    item['avatar_url'] = res['object']['avatar_url'] if res['object']['avatar_url'] else empty_word
                    item['top_answer_count'] = res['object']['top_answer_count'] if res['object'][
                        'top_answer_count'] else empty_word
                    item['topic_url'] = res['object']['url'] if res['object']['url'] else empty_word
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
