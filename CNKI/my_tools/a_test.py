import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
}
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
    # '__': 'Mon Jul 08 2019 14:41:38 GMT+0800 (中国标准时间)',
}
post_url = "https://kns.cnki.net/kns/request/SearchHandler.ashx"
session = requests.session()
a = session.post(url=post_url, headers=headers, data=data).text
cnki_url = "https://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&isinEn=0&dbPrefix=SCOD&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=1562568098139&keyValue=%E5%AE%89%E5%85%A8&S=1&sorttype="
b = session.get(url=cnki_url, headers=headers)
pass
