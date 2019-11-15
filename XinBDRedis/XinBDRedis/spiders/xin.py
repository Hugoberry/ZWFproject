import json
import re
import time
import random
from urllib.parse import quote
import execjs
# import requests
import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisSpider
from XinBDRedis.items import XinbdItem
import redis
from my_tools.ip_test import *

default_value = 'null'
connect = redis.Redis(host='127.0.0.1', port=6379, db=15)
keyword_key = 'keyword_key'
fail_key = 'fail_key'


def analysis_detail_paramenter(r_detail):
    text = r_detail.text
    html = etree.HTML(text)
    d = html.xpath('//*[@id="baiducode"]/text()')[0]
    pid = eval(re.findall(r'"pid":(.*?),.*?"defTags"', text, re.S)[0])
    id1, att = re.findall(r"document\.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)", text)[0]
    tk_func = "function mix(" + re.findall(r'mix\((.*?)\(function', text, re.S)[0]
    tk = re.findall(att + r'="(.*?)">', text)[0]
    tk = execjs.compile(tk_func).call('mix', tk, d)
    time1 = int(time.time() * 1000)
    return pid, tk, time1


class QixinSpider(RedisSpider):
    name = 'XinBDRedis'
    redis_key = 'xin:start_urls'
    allowed_domains = ['baidu.com']
    start_urls = ['https://xin.baidu.com/']

    def parse(self, response):
        for x in range(connect.llen(keyword_key)):
            kw = connect.lindex(keyword_key, 0).decode('utf-8').strip()
            connect.lrem(keyword_key, kw)
            print(kw)
            item = XinbdItem()
            item['search_kw'] = kw
            keyword = quote('%s' % kw)
            nums_url = 'https://xin.baidu.com/s?q=%s&t=0' % keyword
            yield scrapy.Request(url=nums_url, callback=self.parse_first_page, meta={'item': item})

    def parse_first_page(self, response):
        first_urls = 'https://xin.baidu.com/s/l?q={}&t=0&p={}&s=10&o=0&f=undefined&_={}'
        item = response.meta['item']
            # headers = {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
            #                   ' Chrome/70.0.3538.67 Safari/537.36'
            # }
            # proxy = ''
            #
            # ip_ls = [connect.lindex(proxy_key, i).decode('utf-8') for i in range(connect.llen(proxy_key))]
            # print(len(ip_ls))
            # if len(ip_ls) < 5:
            #     get_ip()
            # ip = random.choice(ip_ls)
            # [proxy_host, proxy_port] = re.compile(r'http://(.*?):(\d+)').findall(ip)[0]
            # if not test_ip(proxy_host, proxy_port):
            #     del_to_redis('http://' + proxy_host + ':' + proxy_port)
            # else:
            #     proxy = ip
            # proxies = {
            #     'http': proxy
            # }
            # try:
            #     html = requests.get('https://xin.baidu.com/s?q=%s&t=0' % keyword, headers=headers, proxies=proxies,
            #                         timeout=10).text
            # except Exception as e:
            #     print('keyword is fail!!!  ----  ', kw)
            #     print(e)
            #     connect.lpush('fail_name', kw)
            # else:
        all_page = response.xpath("//div[@class='zx-list-count-left']/em[@class='zx-result-counter']/text()")[0]
        # domain = 'https://xin.baidu.com'
        # pages = ''
        if all_page == '100+':
            pages = 10
        elif all_page == '0':
            pages = 0
        else:
            pages = int(int(all_page) + 1)
        # todo 这里是测试用的， 实际上要换for循环的第一句
        # 在这里只取到了第一页的数据做测试用
        # for page in range(1, 2):
        for page in range(1, pages + 1):
            url = first_urls.format(quote(item['search_kw']), str(page), str(int(time.time() * 1000)))
            # time.sleep(random.random())
            yield scrapy.Request(url=url, callback=self.parse_list_url, meta={'item': item})

    # 解析拿到每页的网址
    def parse_list_url(self, response):
        item = response.meta['item']
        domain = 'https://xin.baidu.com'
        txs = response.text.replace("\\", "")
        par = re.findall(r'''<a class="zx-list-item-url".*?target="_blank".*?href=.*?title=.*?>''', txs, re.DOTALL)
        url_list = [domain + re.search('.*?href="(.*?)" title=.*?', x).group(1) for x in par]
        for url in url_list:
            # time.sleep(random.random())
            yield scrapy.Request(url, callback=self.parse_detail_url, meta={'item': item})
        # 正则解析的模型
        # par = re.compile('"resultList":\[(.*?)\],"totalNumFound":')
        # company_ls = par.findall(response.text)[0]
        # print(company_ls)
        # print(jsonpath.jsonpath())
        # 解析公司列表的模型
        # par_ls = re.compile('{"pid":"(.*?)",'
        #                     '"entName":"(.*?)",'
        #                     '"entType":"(.*?)",'
        #                     '"validityFrom":"(.*?)",'
        #                     '"domicile":"(.*?)",'
        #                     '"entLogo":"(.*?)",'
        #                     '"openStatus":"(.*?)",'
        #                     '"legalPerson":"(.*?)",'
        #                     '"tags":(.*?),'
        #                     '"titleName":"(.*?)",'
        #                     '"titleLegal":"(.*?)",'
        #                     ' "titleDomicile":"(.*?)"')
        # par_ls = re.compile(r'{"pid":"(.*?)",')
        # 在搜索页显示的公司粗略信息
        # print(par_ls.findall(company_ls))

    def parse_detail_url(self, response):
        item = response.meta['item']
        # change_rec = response.xpath('//ul[@class="zx-detail-tab"]/li[2]/span[2]/text()').extract_first()
        # knowledge = response.xpath('//ul[@class="zx-detail-tab"]/li[3]/span[2]/text()').extract_first()
        # relationship = response.xpath('//ul[@class="zx-detail-tab"]/li[4]/span[2]/text()').extract_first()
        # year_report = response.xpath('//ul[@class="zx-detail-tab"]/li[5]/span[2]/text()').extract_first()
        # supervise_info = response.xpath('//ul[@class="zx-detail-tab"]/li[6]/span[2]/text()').extract_first()
        # data_read = response.xpath('//ul[@class="zx-detail-tab"]/li[7]/span[2]/text()').extract_first()
        # praise = response.xpath('//ul[@class="zx-detail-tab"]/li[8]/span[2]/text()').extract_first()
        # todo 解析这些字段， 思路是为0不加网址， 不为零分情况讨论
        # todo 看情况而定
        pid, tk, time1 = analysis_detail_paramenter(response)
        item['pid'] = str(pid)
        item['tot'] = str(tk)
        # print(pid)
        # print(item['tot'])
        url1 = "https://xin.baidu.com/detail/basicAjax?pid={}&tot={}&_={}".format(pid, tk, time1)
        # time.sleep(random.random())
        yield scrapy.Request(url1, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item_one = response.meta['item']
        # print(response.content)
        # 写入文件
        # with open('./DemoHtml/1.json', 'a+') as fw:
        #     fw.write(response.text)
        # 解析详情拿到所有的详情二进制字符串
        html = json.loads(response.text)['data']
        item = XinbdItem()

        item['search_kw'] = item_one['search_kw']

        if 'entLogo' in html:
            item['entLogo'] = html['entLogo']
        else:
            item['entLogo'] = default_value

        if 'shareLogo' in html:
            item['shareLogo'] = html['shareLogo']
        else:
            item['shareLogo'] = default_value

        if 'entName' in html:
            item['entName'] = html['entName']
        else:
            item['entName'] = default_value

        if 'bdCode' in html:
            item['bdCode'] = html['bdCode']
        else:
            item['bdCode'] = default_value

        if 'openStatus' in html:
            item['openStatus'] = html['openStatus']
        else:
            item['openStatus'] = default_value

        if 'entType' in html:
            item['entType'] = html['entType']
        else:
            item['entType'] = default_value

        if 'isClaim' in html:
            item['isClaim'] = html['isClaim']
        else:
            item['isClaim'] = default_value

        if 'claimUrl' in html:
            item['claimUrl'] = html['claimUrl']
        else:
            item['claimUrl'] = default_value

        if 'benchMark' in html:
            item['benchMark'] = html['benchMark']
        else:
            item['benchMark'] = default_value

        if 'regNo' in html:
            item['regNo'] = html['regNo']
        else:
            item['regNo'] = default_value

        if 'orgNo' in html:
            item['orgNo'] = html['orgNo']
        else:
            item['orgNo'] = default_value

        if 'taxNo' in html:
            item['taxNo'] = html['taxNo']
        else:
            item['taxNo'] = default_value

        if 'scope' in html:
            item['scope'] = html['scope']
        else:
            item['scope'] = default_value

        if 'regAddr' in html:
            item['regAddr'] = html['regAddr']
        else:
            item['regAddr'] = default_value

        if 'legalPerson' in html:
            item['legalPerson'] = html['legalPerson']
        else:
            item['legalPerson'] = default_value

        if 'startDate' in html:
            item['startDate'] = html['startDate']
        else:
            item['startDate'] = default_value

        if 'openTime' in html:
            item['openTime'] = html['openTime']
        else:
            item['openTime'] = default_value

        if 'annualDate' in html:
            item['annualDate'] = html['annualDate']
        else:
            item['annualDate'] = default_value

        if 'regCapital' in html:
            item['regCapital'] = html['regCapital']
        else:
            item['regCapital'] = default_value

        if 'industry' in html:
            item['industry'] = html['industry']
        else:
            item['industry'] = default_value

        if 'telephone' in html:
            item['telephone'] = html['telephone']
        else:
            item['telephone'] = default_value

        if 'district' in html:
            item['district'] = html['district']
        else:
            item['district'] = default_value

        if 'authority' in html:
            item['authority'] = html['authority']
        else:
            item['authority'] = default_value

        if 'realCapital' in html:
            item['realCapital'] = html['realCapital']
        else:
            item['realCapital'] = default_value

        if 'orgType' in html:
            item['orgType'] = html['orgType']
        else:
            item['orgType'] = default_value

        if 'scale' in html:
            item['scale'] = html['scale']
        else:
            item['scale'] = default_value

        if 'directors' in html:
            item['directors'] = html['directors']
        else:
            item['directors'] = default_value

        if 'shares' in html:
            item['shares'] = html['shares']
        else:
            item['shares'] = default_value

        if 'districtCode' in html:
            item['districtCode'] = html['districtCode']
        else:
            item['districtCode'] = default_value

        if 'cid' in html:
            item['cid'] = html['cid']
        else:
            item['cid'] = default_value

        if 'website' in html:
            item['website'] = html['website']
        else:
            item['website'] = default_value

        if 'official_flag' in html:
            item['official_flag'] = html['official_flag']
        else:
            item['official_flag'] = default_value

        if 'shidi_pic' in html:
            item['shidi_pic'] = html['shidi_pic']
        else:
            item['shidi_pic'] = default_value

        if 'gongzhonghao' in html:
            item['gongzhonghao'] = html['gongzhonghao']
        else:
            item['gongzhonghao'] = default_value

        if 'xiongzhanghao' in html:
            item['xiongzhanghao'] = html['xiongzhanghao']
        else:
            item['xiongzhanghao'] = default_value

        if 'weibo' in html:
            item['weibo'] = html['weibo']
        else:
            item['weibo'] = default_value

        if 'phoneArr' in html:
            item['phoneArr'] = html['phoneArr']
        else:
            item['phoneArr'] = default_value

        if 'baozhang_flag' in html:
            item['baozhang_flag'] = html['baozhang_flag']
        else:
            item['baozhang_flag'] = default_value

        if 'shidi_flag' in html:
            item['shidi_flag'] = html['shidi_flag']
        else:
            item['shidi_flag'] = default_value

        if 'zixin_flag' in html:
            item['zixin_flag'] = html['zixin_flag']
        else:
            item['zixin_flag'] = default_value

        if 'chengqi_flag' in html:
            item['chengqi_flag'] = html['chengqi_flag']
        else:
            item['chengqi_flag'] = default_value

        if 'v_level' in html:
            item['v_level'] = html['v_level']
        else:
            item['v_level'] = default_value

        if 'v_url' in html:
            item['v_url'] = html['v_url']
        else:
            item['v_url'] = default_value

        yield item
        # par_info = re.compile(r'{"status":0,"msg":"","data":(.*?)}{"status":0,"msg":"","data":')
        # raw_info = par_info.findall(response.text + '}{"status":0,"msg":"","data":')
        # for info in raw_info:
        #     print(info)
        #     item = XinbdItem()
        #     par_all = r'{"entLogo":"(.*?)","shareLogo":"(.*?)","entName":"(.*?)","bdCode":(.*?),' \
        #               r'"openStatus":"(.*?)","entType":"(.*?)","isClaim":(.*?),"claimUrl":"(.*?)",' \
        #               r'"benchMark":(.*?),"regNo":"(.*?)","orgNo":"(.*?)","taxNo":"(.*?)",' \
        #               r'"scope":"(.*?)","regAddr":"(.*?)","legalPerson":"(.*?)","startDate":"(.*?)",' \
        #               r'"openTime":"(.*?)","annualDate":"(.*?)","regCapital":"(.*?)","industry":"(.*?)",' \
        #               r'"telephone":"(.*?)","district":"(.*?)","authority":"(.*?)","realCapital":"(.*?)",' \
        #               r'"orgType":"(.*?)","scale":"(.*?)","directors":(.*?),"shares":(.*?),"districtCode":' \
        #               r'"(.*?)","cid":"(.*?)","website":"(.*?)","official_flag":(.*?),"shidi_pic":(.*?),' \
        #               r'"gongzhonghao":"(.*?)","xiongzhanghao":"(.*?)","weibo":"(.*?)","phoneArr":(.*?),' \
        #               r'"baozhang_flag":(.*?),"shidi_flag":(.*?),"zixin_flag":(.*?),"chengqi_flag":(.*?),' \
        #               r'"v_level":(.*?),"v_url":"(.*?)"}'
        #     try:
        #         print(re.compile(par_all).findall(info)[0])
        #         (entLogo, shareLogo, entName, bdCode, openStatus, entType, isClaim, claimUrl, benchMark, regNo, orgNo,
        #          taxNo, scope, regAddr, legalPerson, startDate, openTime, annualDate, regCapital, industry, telephone,
        #          district, authority, realCapital, orgType, scale, directors, shares, districtCode, cid, website,
        #          official_flag, shidi_pic, gongzhonghao, xiongzhanghao, weibo, phoneArr, baozhang_flag, shidi_flag,
        #          zixin_flag, chengqi_flag, v_level, v_url) = re.compile(par_all).findall(info)[0]
        #         item['entLogo'] = entLogo
        #         item['shareLogo'] = shareLogo
        #         item['entName'] = entName
        #         item['bdCode'] = bdCode
        #         item['openStatus'] = openStatus
        #         item['entType'] = entType
        #         item['isClaim'] = isClaim
        #         item['claimUrl'] = claimUrl
        #         item['benchMark'] = benchMark
        #         item['regNo'] = regNo
        #         item['orgNo'] = orgNo
        #         item['taxNo'] = taxNo
        #         item['scope'] = scope
        #         item['regAddr'] = regAddr
        #         item['legalPerson'] = legalPerson
        #         item['startDate'] = startDate
        #         item['openTime'] = openTime
        #         item['annualDate'] = annualDate
        #         item['regCapital'] = regCapital
        #         item['industry'] = industry
        #         item['telephone'] = telephone
        #         item['district'] = district
        #         item['authority'] = authority
        #         item['realCapital'] = realCapital
        #         item['orgType'] = orgType
        #         item['scale'] = scale
        #         item['directors'] = directors
        #         item['shares'] = shares
        #         item['districtCode'] = districtCode
        #         item['cid'] = cid
        #         item['website'] = website
        #         item['official_flag'] = official_flag
        #         item['shidi_pic'] = shidi_pic
        #         item['gongzhonghao'] = gongzhonghao
        #         item['xiongzhanghao'] = xiongzhanghao
        #         item['weibo'] = weibo
        #         item['phoneArr'] = phoneArr
        #         item['baozhang_flag'] = baozhang_flag
        #         item['shidi_flag'] = shidi_flag
        #         item['zixin_flag'] = zixin_flag
        #         item['chengqi_flag'] = chengqi_flag
        #         item['v_level'] = v_level
        #         item['v_url'] = v_url
        #         print(legalPerson, openStatus, openTime)
        #         yield item
        #     except IndexError:
        #         pass
