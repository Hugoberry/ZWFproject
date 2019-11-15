import time
from urllib.parse import quote

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
}

cap = DesiredCapabilities.PHANTOMJS.copy()

for key, value in headers.items():
    cap['phantomjs.page.customHeaders.{}'.format(
        key)] = value

driver = webdriver.PhantomJS(executable_path="D:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe", desired_capabilities=cap)
driver.get("https://kns.cnki.net/kns/brief/default_result.aspx")

wait = WebDriverWait(driver, 60, 5)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#btnSearch')))
driver.find_element_by_css_selector(".research > .rekeyword").send_keys("物理")
driver.find_element_by_css_selector('#btnSearch').click()
time.sleep(5)
driver.refresh()
cookieJar = dict()
cookies = driver.get_cookies()
for cookie in cookies:
    cookieJar[cookie["name"]] = cookie["value"]
driver.close()

cookie_str = ''
for k, v in cookieJar.items():
    cookie_str += (k + "=" + v + "; ")
cookie_str = cookie_str[:-2]
headers["Cookie"] = cookie_str
post_url = "https://kns.cnki.net/kns/request/SearchHandler.ashx"
session = requests.session()

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
    'txt_1_value1': '安全',
    'txt_1_special1': '%',
    'his': '0',
    'parentdb': 'SCDB',
    '__': 'Mon Jul 08 2019 14:41:38 GMT+0800 (中国标准时间)',
}
a = session.post(url=post_url, headers=headers, data=data).text
cnki_url = "https://kns.cnki.net/kns/brief/brief.aspx?pagename=%s&t=%d&keyValue=%s&S=1&sorttype=" % (a, int(time.time() * 1000), quote('安全'))
b = requests.get(url=cnki_url, headers=headers)
html = etree.HTML(b.text)
url_list = html.xpath("//td/a[@class='fz14']/@href")
for url in url_list:
    url_dict = dict()
    url_param = url.split("&")
    for u in url_param:
        if 'dbcode' in u:
            url_dict['dbcode'] = u
        elif 'dbname' in u:
            url_dict['dbname'] = u
        elif 'filename' in u:
            url_dict['filename'] = u
    new_url = "http://dbpub.cnki.net/grid2008/dbpub/detail.aspx?" + url_dict['dbcode'] + "&" + url_dict['dbname'] + "&" + url_dict['filename']
    c = requests.get(url=new_url, headers=headers)
    pass
