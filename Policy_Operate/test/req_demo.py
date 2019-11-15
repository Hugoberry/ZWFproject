import requests
import time

url_time = int(time.time() * 1000)
url = 'http://www.sipop.cn/patent-interface-web/policy/queryListPolicyOneN?appKey=fichinfoPotal&accessToken' \
      '=POLICY_TOKEN&pageNum=1&pageSize=10&provinceCode=&industryCode=&cityCode=&technicalField=&region=&' \
      'contentAttributeCode=1100%2C1700%2C1800&highFrequencyWords=&orderDesc=desc&_={}'.format(str(url_time))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'Referer': 'http://www.sipop.cn/module/gate/policy/policiesNList.html',
}

text = requests.get(url=url, headers=headers).text
print(text)
