import requests
# import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.67 Safari/537.36',
    'Referer': 'https://cloud.baidu.com/product/bcd/search.html?keyword=quandashi.xyz',
    'Host': 'cloud.baidu.com',
    'Origin': 'https://cloud.baidu.com',
    # 'Cookie': 'BAIDUID=B6750A19BBE1459E5BC313DCC03FE459:FG=1; BIDUPSID=B6750A19BBE1459E5BC313DCC03FE459; PSTM=1540977273; BDUSS=nhYYldPMjNTREZOcUo1Z2g1Vm4wSmVFZWNGN1A2anZwLXNtZX5jaWxFN3BKZ0pjQVFBQUFBJCQAAAAAAAAAAAEAAAAWZqkGNzYzMjYyMTE3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOmZ2lvpmdpbV; BDSFRCVID=BP-sJeC62r2VdRO7gvpc5T0ggemB7ubTH6aoJQsRJzn1nJQxF0n0EG0Pfx8g0Ku-MGdmogKK0mOTHvQP; H_BDCLCKID_SF=tJIO_DPKJC83fP36q4cobnLQKxnOhC62aKDshn-2-hcqEIL4QT5VLJ_HjPrbJMKtQnRM0b55Wx3qMxbSj4QoLTtZ5lQfbjcqMmbD2pn_5h5nhMJF257JDMP0-ljWLPQy523ion6vQpn-VftuD68-j5oXjN-s-bbfHjv-34QH-jrjDnCk-PI33lR3KP6-35KHMNcp_P0KJMbBJRLG353JbPLkhP5Qtl37JD6yXUoE5brSOCbELtQG5jcbXtoxJpOBMnbMopvaKq6hfp6vbURvD-ug3-7qQl8EtRKJVIL5fIvMqRjnMPoKq4u_KxrXb-uXKKOLVMJNLPOkeq8CDxQn3tPZ-NJMaq5yJGPj0b3HWMnGjno2y5jHhP0h0qO2JTOnb2c7KITp2pRpsIJMMl_WbT8U5ecdJT3qaKviaKJEBMb1fxjMe6D2e5Q3jNLsbtQb26r-3--8-bTVHRDk5-Qo-4_eqxby26n22TneaJ5n0-nnhnTdjP-bbUkF5t5mafK8bjQ3KqTyBIbcVRPRy6C-D5v0jatDqbj-5I5H0RO2HtOEDJopqROHhPD_hgT22-usQD6tQhcH0hOWsIOYM5JjjP-nWq7uQ-3q5mOEBpQYMp4M8UodDUC0j6ObjH8fJ6nH5Cn0QJ5JbTr5jJ6P-DTM-t4V-fPX5-RLfabQKtOF5lOTJh0RMtAb-T-syhOX0pOlJ5rqXJnIW4ndMh7-M5bke6bbDaLtJT_sKCPX0n7aKJRqHnRY-P4_h4L3eP5TeRJZ5mAqot_-QJbC8I3T5R3jjq3QbUJ-2xDfbCrnaIQqahcGqUo_24IahxIu2-Dj2jO43bRT0tPy5KJvfj6EQPOVhP-UyN3LWh37bH6TVJO-KKCMhI_mjMK; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=1; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; CAMPAIGN_TRACK=cp%3Aaladdin%7Ckw%3A1564; CAMPAIGN_TRACK_TIME=2018-11-21+08%3A56%3A22; Hm_lvt_28a17f66627d87f1d046eae152a1c93d=1542761781; BAIDU_CLOUD_TRACK_PATH=https://cloud.baidu.com/product/bcd/search.html?keyword=xiaomi.xyz; H_PS_PSSID=1467_21106_20697_27377_26350_27245_22158; Hm_lpvt_28a17f66627d87f1d046eae152a1c93d=1542765002',
    # 'X-Requested-With': 'XMLHttpRequest',
    # 'Accept': 'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Connection': 'keep-alive',
    # 'Content-Length': '68',
    # 'Content-Type': 'application/json',
}
url = 'https://cloud.baidu.com/api/bcd/search/status'
session = requests.session()
# data = {"labels": ["xiaomi"], "tlds": ["xyz"], "domainNames": [], "others": 'false'}
data = {"domainNames": [{"label":"quandashi","tld":"xyz"}]}
# session.headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   'Chrome/70.0.3538.67 Safari/537.36',
#     'Referer': 'https://cloud.baidu.com/product/bcd/search.html?keyword=xiaomi.xyz',
#     'Host': 'cloud.baidu.com',
#     'Origin': 'https://cloud.baidu.com',
# }
text = requests.post(url=url, headers=headers, json=data).text
print(text)
