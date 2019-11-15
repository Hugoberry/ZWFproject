import json

note = '''
    # 这个程序是为了检测得到已经爬取的数据
    # 生成already.txt
'''

raw_file = open('./URL检测/sum_confirm.txt', 'r+', encoding='utf-8')
# contrast_file = open('./domain_retest/retest_domain.txt', 'r+', encoding='utf-8')
already_file = open('./domain_retest/already.txt', 'w+', encoding='utf-8')

# 读取源文件
while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        json_line = json.loads(line, encoding='utf-8')
        kw = json_line['kw']
        domain = json_line['domain']
        already_file.write(kw + '\t' + domain + '\n')

raw_file.close()
# contrast_file.close()
already_file.close()
