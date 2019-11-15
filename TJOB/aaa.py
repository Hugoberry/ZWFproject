from urllib.parse import quote

import requests

url0 = 'https://easy.lagou.com/talent/search/list.htm?pageNo=1&keyword=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98'
url1 = 'https://easy.lagou.com/talent/search/list.json'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '69',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Anit-Forge-Code': '',
    'X-Anit-Forge-Token': '',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://easy.lagou.com',
    'Referer': 'https://easy.lagou.com/talent/search/list.htm?pageNo=1&keyword=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1562747352; _ga=GA1.2.1096635233.1562747352; _gid=GA1.2.918109667.1562747352; sajssdk_2015_cross_new_user=1; user_trace_token=20190710162914-ccb2ad5d-a2ec-11e9-be26-525400f775ce; LGUID=20190710162914-ccb2b04d-a2ec-11e9-be26-525400f775ce; LG_LOGIN_USER_ID=da135f9c2cc0d4544b723d99e5a5027c00d3cd72f41baef312654e1342e349f3; LG_HAS_LOGIN=1; _putrc=9604A1223C22DD90123F89F2B170EADC; login=true; unick=Kaine+Sun; privacyPolicyPopup=false; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAABEJAAGBA5798298DE0FF6ACE3207FF58A5ED16C; mds_login_authToken="f11ptlOWl1Fm8/nT7YzzI/me8vPL/DnwsOjuBEdq+lo9XlJSLYLRiNyQqvXOqjIibdfg9XkZXCa3S51TH9E7WTTjwWI+7XLZuuHeMxsks3iu+2HZYXENEjPYkcCl0g8MASIbMoR+qRITFNCnnNAGSNJLpUznUy4f5siZWXsJL9x4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; mds_u_n=Kaine+Sun; mds_u_ci=564319; mds_u_cn=%5Cu5317%5Cu4eac%5Cu7ef4%5Cu5883%5Cu79d1%5Cu6280%5Cu6709%5Cu9650%5Cu516c%5Cu53f8; mds_u_s_cn=%5Cu7ef4%5Cu5883%5Cu79d1%5Cu6280; gate_login_token=28a2da2576fa07ba6a4239c90202718203a8583e323e38a93c4835f02071b5a3; gray=resume; _ga=GA1.3.1096635233.1562747352; sensorsdata2015session=%7B%7D; Hm_lvt_b53988385ecf648a7a8254b14163814d=1562747393; href=https%3A%2F%2Feasy.lagou.com%2Fdashboard%2Findex.htm%3Ffrom%3Dc_index; accessId=551129f0-7fc2-11e6-bcdb-855ca3cec030; Hm_lvt_bfa5351db2249abae67476f1ec317000=1562747394; Hm_lpvt_bfa5351db2249abae67476f1ec317000=1562747394; LGSID=20190710185213-c68245c3-a300-11e9-a4de-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1562756168; qimo_seosource_551129f0-7fc2-11e6-bcdb-855ca3cec030=%E7%AB%99%E5%86%85; qimo_seokeywords_551129f0-7fc2-11e6-bcdb-855ca3cec030=; X_HTTP_TOKEN=a7326c6759b41d564586572651dfa3c44e8cb53bbc; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2212614946%22%2C%22%24device_id%22%3A%2216bdb0034e6403-0b26947505f88e-e343166-2073600-16bdb0034e7cd6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22m_cf_cpt_baidu_pcbt%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2275.0.3770.100%22%2C%22easy_company_id%22%3A%22564319%22%2C%22lagou_company_id%22%3A%22570828%22%7D%2C%22first_id%22%3A%2216bdb0034e6403-0b26947505f88e-e343166-2073600-16bdb0034e7cd6%22%7D; Hm_lpvt_b53988385ecf648a7a8254b14163814d=1562756853; pageViewNum=7; LGRID=20190710192306-171b6dcf-a305-11e9-a4de-5254005c3644'
}

data = {
    'pageNo': '1',
    'keyword': quote('数据挖掘'),
    'searchVersion': '1',
}

session = requests.session()
a = session.get(url=url0, headers=headers)
t = session.post(url=url1, headers=headers, data=data)
pass
