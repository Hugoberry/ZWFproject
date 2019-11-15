import re

from xpinyin import Pinyin
import requests

out_file = open('./out.txt', 'w+', encoding='utf-8')
domain_type_ls = ['com', 'cn', 'net', 'com.cn', 'org', 'org.cn', 'net.cn']

for domain_type in domain_type_ls:
    domain_type = domain_type.replace('.', '_')
    file = open('./lost_%s_data.txt' % domain_type, 'r+', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        kw = line.replace('"', '').strip()
        kw_pinyin = Pinyin().get_pinyin(kw).replace('-', '').replace(' ', '').replace('.', '').replace('·', '') \
            .replace(' ', '').replace(';', '').lower()
        url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=' + kw_pinyin + '.' + domain_type.replace('_', '.')
        # 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain=nvb&ampnvc.www.net.cn/cgi-bin/check.cgi?area.domain=jingji.com.cn'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }
        content = requests.get(url=url, headers=headers)
        text = content.text
        domain_url = re.compile('area_domain=(.*)').findall(content.url)[0]
        # domain_tp = re.compile(r'.*?\.(.*)').findall(content.url)[0]
        domain_status = re.compile('<original>(.*)</original>').findall(text)[0]
        out_file.write('{"kw": "%s", "domain_url": "%s", "domain_type": "%s", "domain_status": "%s"}' % (kw, domain_url, domain_type.replace('_', '.'), domain_status) + '\n')

        file.close()

print('finished!!!')
out_file.close()
