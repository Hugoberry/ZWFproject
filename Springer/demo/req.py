from urllib.parse import quote

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Cookie": "ASP.NET_SessionId=rwlvqvhr10pte4qyoc1xooql; Ecp_ClientId=2190708120201230715; Ecp_IpLoginFail=19070836.112.7.158; SID_kns=123113; SID_klogin=125141; KNS_SortType=; SID_crrs=125133; RsPerPage=20; SID_krsnew=125134; cnkiUserKey=879fa867-66c0-c7a9-8697-a93dad7177d7; _pk_ses=*"
     }

# url = "https://kns.cnki.net/kns/brief/default_result.aspx"
#
# session = requests.session()
# a = session.get(url=url, headers=headers)
#
url1 = "https://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&isinEn=0&dbPrefix=SCOD&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t=1562556124748&keyValue=%E7%89%A9%E6%B5%81%20%E7%BB%8F%E6%B5%8E&S=1&sorttype="
b = requests.get(url=url1, headers=headers)
pass
