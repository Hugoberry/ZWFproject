import requests

url = 'http://api.zqz510.com//tmof/query?ftxt=&ti=&apS=&pdStart=&pdEnd=&ty=&psty=&law=&litem=&pageNum=3000&callback=_jqjsp&_1544496981097='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Cookie': '_lastEnterDay=2018-12-11; _cliid=5VvVudZ1LvXdy-13; _siteStatId=1f84349f-3e84-421f-bfe3-bdfdcbb7510c; _siteStatDay=20181211; _siteStatRedirectUv=redirectUv_17361940; _siteStatVisitorType=visitorType_17361940; _siteStatVisit=visit_17361940; _siteStatVisitTime=1544495760792; JSESSIONID=906E525D49196B58DC69D39D5510C641; uid=a4839a86-dcf1-45c8-8bc3-0c1ce6cdf0c1; oid=UAGAP00003921; c=ede59026-eac6-432d-a715-735e838e7185'
}

text = requests.get(url=url, headers=headers).text
print(text)
