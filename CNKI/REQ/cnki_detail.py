import random

import requests
from lxml import etree

from REQ.ip_test import IpTest


class GetDetail(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        }
        self.ip_test = IpTest()
        self.connect = self.ip_test.connect
        self.proxy_key = self.ip_test.proxy_key
        self.ip_test.get_ip()
        self.ip_ls = [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in
                      range(self.connect.llen(self.proxy_key))]
        self.ip = random.choice(self.ip_ls)
        self.proxies = {
            'http': self.ip,
        }
        self.file = open('./cnki_det.txt', mode='a+', encoding='utf-8')
        self.ua_ls = self.ua_list()

    @staticmethod
    def ua_list():
        ua_file = open('./ua.txt', mode='r+', encoding='utf-8')
        ua_ls = []
        while True:
            lines = ua_file.readlines(1024)
            if not lines:
                break
            for line in lines:
                ua_ls.append(line.replace('\n', ''))
        return ua_ls

    def get_detail(self, url):
        headers = {
            "User-Agent": random.choice(self.ua_ls),
        }
        detail_page = None
        try:
            detail_page = requests.get(url=url, headers=headers, proxies=self.proxies, timeout=10)
            if "信息提示" in detail_page.text:
                ips = int(self.connect.llen(self.proxy_key))
                for i in range(ips):
                    self.connect.lpop(self.proxy_key)
                self.ip_test.get_ip()
                self.ip_ls = [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in
                              range(self.connect.llen(self.proxy_key))]
                self.ip = random.choice(self.ip_ls)
                self.proxies = {
                    'http': self.ip,
                }
                self.get_detail(url)
        except Exception as e:
            print(e)
            ips = int(self.connect.llen(self.proxy_key))
            for i in range(ips):
                self.connect.lpop(self.proxy_key)
            self.ip_test.get_ip()
            self.ip_ls = [self.connect.lindex(self.proxy_key, i).decode('utf-8') for i in
                          range(self.connect.llen(self.proxy_key))]
            self.ip = random.choice(self.ip_ls)
            self.proxies = {
                'http': self.ip,
            }
            self.get_detail(url=url)
        self.parse_detail(detail_page)

    def parse_detail(self, response):
        html = etree.HTML(response.text)
        tr = html.xpath("//table[@id='box']/tr")
        data = dict()
        data['link'] = response.url
        for td in tr:
            td_ls = td.xpath("./td/text()")
            if len(td_ls) == 4:
                data[td_ls[0].replace("【", "").replace("】", "").strip()] = td_ls[1].replace("'", "’").replace(":", "：").strip()
                data[td_ls[2].replace("【", "").replace("】", "").strip()] = td_ls[3].replace("'", "’").replace(":", "：").strip()
            elif len(td_ls) == 2:
                data[td_ls[0].replace("【", "").replace("】", "").strip()] = td_ls[1].replace("'", "’").replace(":", "：").strip()

        self.file.write(str(data) + "\n")


if __name__ == '__main__':
    g = GetDetail()
    raw_file = open("./unsp.txt", mode="r+", encoding="utf-8")
    while True:
        lines = raw_file.readlines(4096)
        if not lines:
            break
        for line in lines:
            g.get_detail(line.replace("\n", ""))
