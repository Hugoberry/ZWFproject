import random
import re
import time
from urllib.parse import quote

import requests

from lxml import etree

from REQ.ip_test import IpTest


class CNKISpider(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }
        self.ip_test = IpTest()
        self.connect = self.ip_test.connect
        self.proxy_key = self.ip_test.proxy_key
        self.ip_test.get_ip()
        self.ip_ls = [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in range(self.connect.llen(self.proxy_key))]
        self.ip = random.choice(self.ip_ls)
        self.proxies = {
            'http': self.ip,
        }
        self.file = open('./cnki_data.txt', mode='a+', encoding='utf-8')

    def get_cookies(self, kw):

        data = {
            'action': '',
            'ua': '1.11',
            'isinEn': '0',
            'PageName': 'ASP.brief_default_result_aspx',
            'DbPrefix': 'SCOD',
            'DbCatalog': '中国学术文献网络出版总库',
            'ConfigFile': 'SCDBINDEX.xml',
            'db_opt': 'SCOD',
            'txt_1_sel': 'SU$%=|',
            'txt_1_value1': '%s' % kw,
            'txt_1_special1': '%',
            'his': '0',
            'parentdb': 'SCDB',
        }
        post_url = "https://kns.cnki.net/kns/request/SearchHandler.ashx"

        session = requests.session()
        ck = session.post(url=post_url, data=data, headers=self.headers, proxies=self.proxies)
        url_str = ck.text
        cnki_url = "https://kns.cnki.net/kns/brief/brief.aspx?pagename=%s&t=%d&keyValue=%s&S=1&sorttype=" % (
            url_str, int(time.time() * 1000), quote(kw))
        res = session.get(url=cnki_url, headers=self.headers, proxies=self.proxies)
        return res, session, kw

    def parse_list(self, response, session, kw):
        referer = response.url
        res = etree.HTML(response.text)
        self.parse_detail(res, kw)
        try:
            pages = res.xpath("//span[@class='countPageMark']/text()")[0].replace('1/', '')
            for page in range(2, int(pages) + 1):
                url = "https://kns.cnki.net/kns/brief/brief.aspx?curpage=%d&RecordsPerPage=20&QueryID=3&ID=&turnpage=1" \
                      "&tpagemode=L&dbPrefix=SCOD&Fields=&DisplayMode=listmode&PageName=ASP.brief_default_result_aspx" \
                      "&sKuaKuID=3&isinEn=0&" % page
                self.headers['Referer'] = referer

                resp = session.get(url=url, headers=self.headers, proxies=self.proxies)
                resp = etree.HTML(resp.text)
                self.parse_detail(resp, kw)
        except IndexError:
            pass

    def parse_detail(self, response, kw):
        tr = response.xpath('//tr[@bgcolor="#ffffff"] | //tr[@bgcolor="#f6f7fb"]')
        for td in tr:
            data_dict = dict()
            data_dict['kw'] = kw
            c_no = td.xpath('./td[1]/text()')[0]
            data_dict['c_no'] = c_no

            name = td.xpath('./td[2]/a')[0].xpath('string(.)').strip()
            try:
                name = re.compile(r'target="_blank">(.*?)</a>').findall(name)[0].replace('<font class="Mark">',
                                                                                         "").replace('</font>', "")
            except IndexError:
                name = name

            data_dict['name'] = name

            url_dict = dict()
            url_param = td.xpath('./td[2]/a/@href')[0].split("&")
            for u in url_param:
                if 'dbcode' in u:
                    url_dict['dbcode'] = u
                elif 'dbname' in u:
                    url_dict['dbname'] = u
                elif 'filename' in u:
                    url_dict['filename'] = u
            link = "http://dbpub.cnki.net/grid2008/dbpub/detail.aspx?" + url_dict['dbcode'] + "&" + url_dict[
                'dbname'] + "&" + url_dict['filename']
            data_dict['link'] = link
            inventor = td.xpath('./td[3]/text()')[0]
            data_dict['inventor'] = inventor
            applicant = td.xpath('./td[4]/text()')[0]
            data_dict['applicant'] = applicant
            source_from = td.xpath('./td[5]/text()')[0]
            data_dict['source_from'] = source_from
            apply_date = td.xpath('./td[6]/text()')[0]
            data_dict['apply_date'] = apply_date
            pub_date = td.xpath('./td[7]/text()')[0]
            data_dict['pub_date'] = pub_date
            self.file.write(str(data_dict) + '\n')

    def run(self, k):
        res, session, kw = self.get_cookies(k)
        try:
            self.parse_list(res, session, kw)
        except Exception as e:
            print(e)
            self.connect.lpop(self.proxy_key)
            self.ip_test.get_ip()
            self.ip_ls = [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in
                          range(self.connect.llen(self.proxy_key))]
            self.ip = random.choice(self.ip_ls)
            self.proxies = {
                'http': self.ip,
            }
            self.run(k)


if __name__ == '__main__':
    c = CNKISpider()
    raw_file = open('./cnki_kw.txt', mode='r+', encoding='utf-8')
    while True:
        lines = raw_file.readlines(4096)
        if not lines:
            break
        for line in lines:
            kwd = line.replace('\n', '')
            c.run(kwd)
