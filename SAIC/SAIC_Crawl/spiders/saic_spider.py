# -*- coding: utf-8 -*-
import scrapy
import re

from SAIC_Crawl.items import SaicCrawlItem

empty_word = 'null'


class SaicSpiderSpider(scrapy.Spider):
    name = 'saic_spider'
    allowed_domains = ['saic.gov.cn']
    start_urls = ['http://wssq.saic.gov.cn:9080/tmsve/#']

    def parse(self, response):
        url = 'http://wssq.saic.gov.cn:9080/tmsve/pingshen_getMain.xhtml'
        yield scrapy.Request(url=url, callback=self.parse_data)
        yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_data(self, response):
        url = 'http://wssq.saic.gov.cn:9080/tmsve/pingshen_getMain.xhtml'
        total_sum = response.xpath('//center/nobr/input[@name="sum"]/@value').extract_first()
        countpage = response.xpath('//center/nobr/input[@name="countpage"]/@value').extract_first()
        for num in range(int(total_sum)):
            data = {
                'param.regNum': '',
                'param.tmName': '',
                'param.appCnName': '',
                'param.objAppCnName': '',
                'param.agentName': '',
                'param.startDate': '',
                'param.endDate': '',
                'pagenum': '%s' % str(num + 1),
                'pagesize': '30',
                'sum': '%s' % total_sum,
                'countpage': '%s' % countpage,
                'gopage': '3',
            }
            yield scrapy.FormRequest(url=url, method='POST', formdata=data, callback=self.parse_list)

    def parse_list(self, response):
        # page_ls = response.xpath('//div[@class="link"]/table/tbody/tr')
        page_ls = response.xpath('//div[@class="link"]/tr/td/table/tbody/tr')
        for page in page_ls:
            item = SaicCrawlItem()

            title = page.xpath('./td[2]/a/p/text()').extract_first()
            link = 'http://wssq.saic.gov.cn:9080' + page.xpath('./td[2]/a/@href').extract_first().replace('\n', '')
            date = page.xpath('./td[2]/p[2]/text()').extract_first()
            judge_type = title.split('商标')[1][:-3]
            item['judge_type'] = judge_type

            item['title'] = title
            item['link'] = link
            item['date'] = date

            yield scrapy.Request(url=link, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):

        page = response.xpath('//div[@class="TRS_Editor"]')

        for pg in page:
            item = response.meta['item']
            case_no = pg.xpath('./p[3]/span/font/text()').extract_first()
            pg_content = pg.xpath('./p[5]/span/font').extract_first()
            case_icon_ls = pg.xpath('./p[5]/span/font/span/a/text()').extract()
            case_icon_link_ls = pg.xpath('./p[5]/span/font/span/@myvalue').extract()

            item['case_no'] = case_no
            item['pg_content'] = pg_content
            item['case_icon'] = str(case_icon_ls)
            item['case_icon_link'] = str(case_icon_link_ls)

            applicator = re.compile(r'申请人(.*?)<br>').findall(pg_content)

            if applicator:
                item['applicator'] = applicator[0].replace('：', ' ')
            else:
                item['applicator'] = empty_word

            proxies = re.compile(r'委托代理人：(.*?)<br>').findall(pg_content)

            if proxies:
                item['proxies'] = proxies[0]
            else:
                item['proxies'] = empty_word

            by_applicator = re.compile(r'被申请人\(原撤销申请人\)：(.*?)<br>').findall(pg_content)

            if by_applicator:
                item['by_applicator'] = by_applicator[0].replace('：', ' ')
            else:
                item['by_applicator'] = empty_word

            judge_relay = re.compile(r'依照(.*)的规定').findall(pg_content)

            if judge_relay:
                item['judge_relay'] = judge_relay[0]
            else:
                item['judge_relay'] = empty_word

            member = pg.xpath('./p[6]/span/font').extract_first()
            if '合议组成员:' in member:
                member_ls = member.split('合议组成员:')[1].split('</font>')[0].split('<br>')
                item['member'] = str(member_ls)
            else:
                item['member'] = member.split('独任审查员:')[1].split('</font>')[0]

            if re.compile(r'复审商标予以撤销。').findall(pg_content):
                item['judge_status'] = '失败'
            elif re.compile(r'争议商标予以无效宣告。').findall(pg_content):
                item['judge_status'] = '成功'
            else:
                item['judge_status'] = '部分成功'

            server_range = re.compile(r'申请商标指定使用在(.*)上的注册申请予以初步审定').findall(pg_content)
            if server_range:
                item['server_range'] = server_range[0]
            else:
                item['server_range'] = empty_word

            yield item
