import os
import json

'''
    # 这个程序是为了找出需要检测的全部网址并且得到对应的关键字
    # 主要是判断得到的数据对应的网域状态码是不是211开头
    # 211开头说明网域名存在, 其他状态码是错的
    # retest_domain.txt 是需要检测的网域的集合
'''
if not os.path.exists('./domain_retest/'):
    os.makedirs('./domain_retest/')

new_file = open('./domain_retest/retest_domain.txt', 'w+', encoding='utf-8')
raw_file = open('./domain_sum.txt', 'r+', encoding='utf-8')

while True:
    lines = raw_file.readlines(4096)
    try:
        for line in lines:
            json_line = json.loads(line, encoding='utf-8')
            domain_status = json_line['domain_status']
            if domain_status.startswith('211'):
                kw = json_line['kw']
                domain_url = json_line['domain_url']
                new_file.write(kw + '\t' + domain_url + '\n')
            else:
                pass
    except Exception as e:
        print(e)

    if not lines:
        break

new_file.close()
raw_file.close()
print('finished!!!')
