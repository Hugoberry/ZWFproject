# -*- coding: utf-8 -*-
from urllib.parse import quote

import redis
import scrapy
from scrapy_redis.spiders import RedisSpider

from Springer.items import SpringerItem

empty_word = 'null'
keyword_key = 'keyword_key'


class SpringerSpider(RedisSpider):
    name = 'springer'
    allowed_domains = ['springer.com']
    start_urls = ['https://link.springer.com/']
    redis_key = 'springer:start_urls'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_connect_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=15)
        self.connect = redis.StrictRedis(connection_pool=self.redis_connect_pool, decode_responses=True)

        # https://link.springer.com/search?date-facet-mode=between&facet-content-type=%22ConferencePaper%22&query=ali&facet-end-year=2013&facet-start-year=2013
        # https://link.springer.com/search?query=ali&date-facet-mode=between&facet-end-year=2013&facet-start-year=2013&facet-content-type=%22Article%22
        # https://link.springer.com/search/page/2?date-facet-mode=between&facet-content-type=%22ConferencePaper%22&query=ali&facet-end-year=2013&facet-start-year=2013

        self.empty_word = "null"
        # self.headers = {
        #     "Referer": "https://link.springer.com/search?query={}&facet-content-type=%22Article%22".format(''),
        #     "Upgrade-Insecure-Requests": "1",
        #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) "
        #                   "Chrome/75.0.3770.100 Safari/537.36",
        # }

    def parse(self, response):
        years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
        needs = ['Article', 'ConferencePaper']

        while True:
            try:
                keyword = self.connect.blpop(keyword_key, timeout=60)[1].decode('utf-8').strip()
                # keyword = 'AI'
                for x in needs:
                    for i in years:
                        print(x, i)
                        url = "https://link.springer.com/search?query={}&date-facet-mode=between&facet-end-year={}&facet" \
                              "-start-year={}&facet-content-type=%22{}%22".format(quote(keyword), str(i), str(i), x)
                        yield scrapy.Request(url=url, callback=self.parse_pages, meta={
                            'need': x, 'year': i, 'keyword': keyword})
            except TypeError:
                break

    def parse_pages(self, response):
        need = response.meta['need']
        year = response.meta['year']
        keyword = response.meta['keyword']
        pages = response.xpath('//span[@class="number-of-pages"]/text()').extract_first().replace(",", "")
        pages = int(pages)
        # for i in range(1, int(pages) + 1):
        if pages >= 1000:
            pages = 1000
        for i in range(1, pages):
            if i == 1:
                yield scrapy.Request(url=response.url, callback=self.parse_list, meta={
                        'need': need, 'year': year, 'keyword': keyword, 'page': i})
            else:
                url = "https://link.springer.com/search/page/{}?date-facet-mode=between&facet-content-type=%22{}%22" \
                      "&query={}&facet-end-year={}&facet-start-year={}".format(str(i), need, keyword, year, year)
                yield scrapy.Request(url=url, callback=self.parse_list, meta={
                        'need': need, 'year': year, 'keyword': keyword, 'page': i})

    def parse_list(self, response):
        need = response.meta['need']
        page = response.meta['page']
        keyword = response.meta['keyword']
        year = response.meta['year']
        links = response.xpath('//ol[@id="results-list"]//h2/a/@href').extract()
        for link in links:
            x = links.index(link)
            url = "https://link.springer.com" + link
            yield scrapy.Request(url=url, callback=self.parse_detail, meta={
                        'need': need, 'keyword': keyword, 'year': year, 'page': page, 'index': x})

    def parse_detail(self, response):
        need = response.meta['need']
        year = response.meta['year']
        page = response.meta['page']
        p_index = response.meta['index']
        search_kw = response.meta['keyword']

        with open('./HTMLS/{}_{}_{}_{}_{}.html'.format(quote(search_kw).replace('/', '-'), need, year, page, p_index), mode='w+', encoding='utf-8') as fw:
            fw.write(response.text)

        item = SpringerItem()

        item['search_kw'] = search_kw
        item['need'] = need
        item['year'] = year
        item['page'] = page
        item['p_index'] = p_index
        item['status'] = 'success'

        yield item

        # ---------------------------分割线--------------------------
        # item['search_kw'] = search_kw
        # item['need'] = need
        # journal_title = response.xpath('//div[@id="enumeration"]/p[1]/a/@title').extract_first()
        # articleCitation_year = response.xpath(
        #     '//div[@id="enumeration"]/p[2]/span[@class="ArticleCitation_Year"]/time/text()').extract_first()
        # articleCitation_volume = response.xpath(
        #     '//div[@id="enumeration"]/p[2]/span[@class="ArticleCitation_Volume"]/text()').extract_first()
        # articleCitation_issue = response.xpath(
        #     '//div[@id="enumeration"]/p[2]/a[@class="ArticleCitation_Issue"]/text()').extract_first()
        # articleCitation_pages = response.xpath(
        #     '//div[@id="enumeration"]/p[2]/span[@class="ArticleCitation_Pages"]/text()').extract_first()
        # article_title = response.xpath('//div[@class="MainTitleSection"]/h1[@class="ArticleTitle"]/text()').extract_first()
        #
        # test_contributor_names = response.xpath(
        #     '//ul[@class="test-contributor-names"]/li[@itemtype="http://schema.org/Person"]')
        # contributor_names = []
        # for c_name in test_contributor_names:
        #     authors_affiliations_name = c_name.xpath('./span[@itemprop="name"]/text()').extract_first()
        #     authors_affiliations_name = authors_affiliations_name if authors_affiliations_name else self.empty_word
        #     authors_affiliations_indexes = c_name.xpath('./ul[@data-role="AuthorsIndexes"]/li/text()').extract_first()
        #     if authors_affiliations_indexes:
        #         a_index = ",".join(authors_affiliations_indexes)
        #         contributor_names.append(
        #             {"authors_affiliations_name": authors_affiliations_name, "authors_affiliations_indexes": a_index})
        #
        # affiliations = []
        # affiliation_list = response.xpath('//ol[@class="test-affiliations"]/li')
        # for affiliation in affiliation_list:
        #     affiliation_count = affiliation.xpath('./span[@class="affiliation__count"]/text()').extract_first()
        #     affiliation_count = affiliation_count if affiliation_count else self.empty_word
        #     affiliation_name = affiliation.xpath(
        #         './span[@class="affiliation__item"]/span[@class="affiliation__name"]/text()').extract_first()
        #     affiliation_name = affiliation_name if affiliation_name else self.empty_word
        #     affiliation_address = affiliation.xpath(
        #         './span[@class="affiliation__item"]/span[@class="affiliation__address"]/span/text()').extract_first()
        #     affiliation_address = ",".join(affiliation_address)
        #     affiliations.append(affiliation_count + affiliation_name + "," + affiliation_address)
        #
        # downloads = response.xpath(
        #     '//div[@class="main-context__container"]/div[@class="main-context__column"]/ul/li[1]/span[1]/text()').extract_first()
        # citations = response.xpath(
        #     '//div[@class="main-context__container"]/div[@class="main-context__column"]/ul/li[2]/a/span[1]/text()').extract_first()
        # abstract = response.xpath('//section[@class="Abstract"]/p[@id="Par1"]/text()').extract_first()
        # keywords = response.xpath('//div[@class="KeywordGroup"]/span[@class="Keyword"]/text()').extract()
        # keywords = ", ".join(keywords).replace("&nbsp;", " ")
        # refSource = response.xpath('//div[@class="HeaderArticleNotes"]//a[@rel="noopener"]/span/text()').extract_first()
        # references = response.xpath('//ol[@class="BibliographyWrapper"]/li[@class="Citation"]/div[@class="CitationContent"]/text()').extract()
        #
        # item['journal_title'] = journal_title
        # item['articleCitation_year'] = articleCitation_year
        # item['articleCitation_volume'] = articleCitation_volume
        # item['articleCitation_issue'] = articleCitation_issue
        # item['articleCitation_pages'] = articleCitation_pages
        # item['article_title'] = article_title
        # # item['test_contributor_names'] = test_contributor_names
        # item['contributor_names'] = contributor_names
        # item['affiliations'] = affiliations
        # item['downloads'] = downloads
        # item['citations'] = citations
        # item['abstract'] = abstract
        # item['keywords'] = keywords
        # item['refSource'] = refSource
        # item['references'] = str(references)
        #
        # yield item
