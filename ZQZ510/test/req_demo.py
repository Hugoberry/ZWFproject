import requests

url = 'http://api.zqz510.com//tmof/query?ftxt=&ti=&apS=&pdStart=&pdEnd=&ty=&psty=&law=&litem=&pageNum=1&apS=&apD=&ag=&judgd=&tid=&cid=&callback=_jqjsp&_1544409929964='
headers = {
    'Cookie': 'JSESSIONID=8CB74C9A33BEABA489F276CBAFBD554A; uid=213facea-5ac7-4069-ae4a-97168d559ebc; oid=UAGAP00003919; c=29b6c55b-065a-4eab-bad4-8ea7e750aa49',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

text = requests.get(url=url, headers=headers).text
print(text)
