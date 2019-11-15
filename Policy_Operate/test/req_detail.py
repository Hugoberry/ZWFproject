import requests
import time

url_time = int(time.time() * 1000)
url = 'http://www.sipop.cn/patent-interface-web/policy/getPolicyWithPolicyId?appKey=fichinfoPotal&access' \
      'Token=POLICY_TOKEN&policyId=78c536c8-b370-4fce-9c2f-8361d478e179&_=_={}'.format(str(url_time))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    # 'Referer': 'http://www.sipop.cn/module/gate/policy/policiesNList.html',
}

text = requests.get(url=url, headers=headers).text
print(text)
