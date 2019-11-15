import asyncio

import requests
from lxml import etree


class SpringerSpider:

    def __init__(self):
        self.keyword = "knowledge graph".replace(" ", "+")
        self.url = "https://link.springer.com/search?query={}&facet-content-type=%22Article%22".format(self.keyword)
        self.empty_word = "null"
        self.headers = {
            "Referer": "https://link.springer.com/search?query=%s" % self.keyword,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/75.0.3770.100 Safari/537.36",
        }

        self.file = open("./springer_data.txt", mode="a+", encoding="utf-8")
    
    def get_pages(self, first_url):
        text = requests.get(url=first_url, headers=self.headers).text
        html = etree.HTML(text)
        pages = html.xpath('//span[@class="number-of-pages"]/text()')[0].replace(",", "")
        return int(pages)
    
    def get_list(self):
        pages = self.get_pages(self.url)
        for i in range(1, pages + 1):
            if i == 1:
                text = requests.get(url=self.url, headers=self.headers).text
                html = etree.HTML(text)
                paper_link = html.xpath('//ol[@id="results-list"]//h2/a/@href')
                self.get_detail(paper_link) 
            else:
                url = "https://link.springer.com/search/page/{}?facet-content-type=%22Article%22&query={}".format(str(i), self.keyword)
                text = requests.get(url=url, headers=self.headers).text
                html = etree.HTML(text)
                paper_link = html.xpath('//ol[@id="results-list"]//h2/a/@href')
                self.get_detail(paper_link) 
    
    def get_detail(self, papers_link):
        loop = asyncio.get_event_loop()
        for link in papers_link:
            loop.run_until_complete(self.parse_detail(link))

    async def parse_detail(self, link):

        link = "https://link.springer.com" + link
        paper_text = requests.get(url=link, headers=self.headers).text

        paper_html = etree.HTML(paper_text)
        journal_title = paper_html.xpath('//div[@id="enumeration"]/p[1]/a/@title')
        articleCitation_year = paper_html.xpath('//div[@id="enumeration"]/p[2]/span[@class="ArticleCitation_Year"]/time/text()')
        articleCitation_volume = paper_html.xpath('//div[@id="enumeration"]/p[2]/span[@class="ArticleCitation_Volume"]/text()')
        articleCitation_issue = paper_html.xpath('//div[@id="enumeration"]/p[2]/a[@class="ArticleCitation_Issue"]/text()')
        articleCitation_pages = paper_html.xpath('//div[@id="enumeration"]/p[2]/span[@class="ArticleCitation_Pages"]/text()')
        article_title = paper_html.xpath('//div[@class="MainTitleSection"]/h1[@class="ArticleTitle"]/text()')
        
        test_contributor_names = paper_html.xpath('//ul[@class="test-contributor-names"]/li[@itemtype="http://schema.org/Person"]')
        contributor_names = [] 
        for c_name in test_contributor_names:
            authors_affiliations_name = c_name.xpath('./span[@itemprop="name"]/text()')
            authors_affiliations_name = authors_affiliations_name[0] if authors_affiliations_name else self.empty_word
            authors_affiliations_indexes = c_name.xpath('./ul[@data-role="AuthorsIndexes"]/li/text()')
            if authors_affiliations_indexes:
                a_index = ",".join(authors_affiliations_indexes)
                contributor_names.append({"authors_affiliations_name": authors_affiliations_name, "authors_affiliations_indexes": a_index})
        
        affiliations = []
        affiliation_list = paper_html.xpath('//ol[@class="test-affiliations"]/li')
        for affiliation in affiliation_list:
            affiliation_count = affiliation.xpath('./span[@class="affiliation__count"]/text()')
            affiliation_count = affiliation_count[0] if affiliation_count else self.empty_word
            affiliation_name = affiliation.xpath('./span[@class="affiliation__item"]/span[@class="affiliation__name"]/text()')
            affiliation_name = affiliation_name[0] if affiliation_name else self.empty_word
            affiliation_address = affiliation.xpath('./span[@class="affiliation__item"]/span[@class="affiliation__address"]/span/text()')
            affiliation_address = ",".join(affiliation_address)
            affiliations.append(affiliation_count + affiliation_name + "," + affiliation_address)
        
        downloads = paper_html.xpath('//div[@class="main-context__container"]/div[@class="main-context__column"]/ul/li[1]/span[1]/text()')
        citations = paper_html.xpath('//div[@class="main-context__container"]/div[@class="main-context__column"]/ul/li[2]/a/span[1]/text()')
        abstract = paper_html.xpath('//section[@class="Abstract"]/p[@id="Par1"]/text()')
        keywords = paper_html.xpath('//div[@class="KeywordGroup"]/span[@class="Keyword"]/text()')
        keywords = ", ".join(keywords).replace("&nbsp;", " ")
        refSource = paper_html.xpath('//div[@class="HeaderArticleNotes"]//a[@rel="noopener"]/span/text()')
        
        info = {
            'journal_title': journal_title[0] if journal_title else self.empty_word,
            'articleCitation_year': articleCitation_year[0] if articleCitation_year else self.empty_word,
            'articleCitation_volume': articleCitation_volume[0] if articleCitation_volume else self.empty_word,
            'articleCitation_issue': articleCitation_issue[0] if articleCitation_issue else self.empty_word,
            'articleCitation_pages': articleCitation_pages[0] if articleCitation_pages else self.empty_word,
            'article_title': article_title[0] if article_title else self.empty_word,
            'contributor_names': contributor_names,
            'affiliations': affiliations,
            'downloads': downloads[0] if downloads else self.empty_word,
            'citations': citations[0] if citations else self.empty_word,
            'abstract': abstract[0] if abstract else self.empty_word,
            'keywords': keywords[0] if keywords else self.empty_word,
            'refSource': refSource[0] if refSource else self.empty_word,
        }
        self.file.write(str(info) + "\n")
        self.file.flush()
    
    def run(self):
        self.get_list()
        self.file.close()


if __name__ == "__main__":
    ss = SpringerSpider()
    ss.run()
