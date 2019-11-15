import requests

url = 'http://wssq.saic.gov.cn:9080/tmsve/pingshen_getMain.xhtml'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
data = {
'param.regNum': '',
'param.tmName': '',
'param.appCnName': '',
'param.objAppCnName': '',
'param.agentName': '',
'param.startDate': '',
'param.endDate': '',
'pagenum': '4',
'pagesize': '30',
'sum': '223954',
'countpage': '7466',
'gopage': '3',
}
text = requests.post(url=url, headers=headers, json=data).text
print(text)
