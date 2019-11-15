# -*- coding: utf-8 -*-
import re

import requests
import scrapy
from urllib.parse import quote
from JDspider.items import JdspiderItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&enc=utf-8&'
                  'spm=a.0.0&wq=&pvid=b4fc608c955e47f69935548ef366dbbe']

    def parse(self, response):
        file = open(r'C:\\Users\\Administrator\\Desktop\\a.txt', 'r+')
        line = file.readlines()
        len_len = len(line)
        for word in range(len_len):
            kw = line[word].replace('(', '').replace(',1)', '').strip()
            print(kw)
            url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=bjb&pvid=39022e74e5c345b5955e121fdca8' \
                  '49b7' % quote(kw)
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        url_ls = response.xpath('//div[@class="p-name p-name-type-2"]/a/@href').extract()
        if url_ls == []:
            pass
        else:
            for url in url_ls:
                print(url)
                url = 'https:' + url
                yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        namelist= []
        contentlist = []

        item = JdspiderItem()
        infolist = response.xpath('//*[@id="detail"]/div[2]/div')
        name = response.xpath('//div[@class="w"]//div[@class="sku-name"]/text()').extract_first().strip()
        # if not name:
        #     pass
        # else:
        #     name = name[0].strip()
        #     print(name)

        # print("商品名称：", name)
        namelist.append("商品名称")
        contentlist.append(name)
        # item['name'] = name

        try:
            shopping_info = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').extract()[1:-1]
            for i in shopping_info:
                namelist.append("商品其他信息")
                contentlist.append(i + '\t')
        except:
            baozhuang = "未列明"

        # print("包装清单：", baozhuang)
        # namelist.append("包装清单")
        # contentlist.append(baozhuang)

        # jieshao = html.xpath("//div[@class='item hide']/text()")[0]
        # print("商品简介：",jieshao)

        # 京东的价格采用ajax动态加载，而且同一IP请求过于频繁可能触发验证码，这里很坑
        # 如果触发验证码则获取不到价格信息，暂时没找到好的解决办法，添加异常处理

        try:
            number = re.findall(r"com/(\d+)\.html", response.url)[0]
            # print(number)

            ajaxUrl = r"https://p.3.cn/prices/mgets?pdtk=&skuIds=J_" + number

            ajaxResponse = requests.get(ajaxUrl)
            # print(ajaxResponse.text)
            prices = re.findall('"p":"(.*?)"', ajaxResponse.text)[0].strip()
            # print("价格：", prices)

        except:
            prices = "获取失败"

        namelist.append("价格")
        contentlist.append(prices)

        for info in infolist:
            titles = info.xpath('./div[@class="p-parameter"]/ul[2]/li[1]/a/text()')
            contents = info.xpath('/div[@class="p-parameter"]/ul[3]/li[1]/text()')
            for title, content in zip(titles, contents):
                # print(title, ':', content)
                namelist.append(title.strip())
                contentlist.append(content.strip())

        item['name'] = namelist
        item['content'] = contentlist
        item['url'] = response.url

        yield item


