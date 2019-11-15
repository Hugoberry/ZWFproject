import re
import json

base_file = open('./交易库商标名称名录.txt', 'r+', encoding='utf-8')
base_set = set()
while True:
    lines = base_file.readlines(4096)
    for line in lines:
        word = re.compile('"(.*)"').findall(line)[0]
        base_set.add(word)
    if not lines:
        break

contrast_file = open('./网域数据/domain_sum.txt', 'r+', encoding='utf-8')

# 在这里把所有的网域都做成字典检测哪些没有爬取
# ['com', 'cn', 'net', 'com.cn', 'org', 'org.cn', 'net.cn']
com_set = set()
cn_set = set()
com_cn_set = set()
net_set = set()
org_set = set()
org_cn_set = set()
net_cn_set = set()

while True:
    contrast_lines = contrast_file.readlines(4096)
    for line in contrast_lines:
        try:
            word = json.loads(line, encoding='utf-8')
            kw = word['kw']
            tp = word['domain_type']
            if tp == 'com':
                com_set.add(kw + ':' + tp)
            elif tp == 'cn':
                cn_set.add(kw + ':' + tp)
            elif tp == 'com.cn':
                com_cn_set.add(kw + ':' + tp)
            elif tp == 'org':
                org_set.add(kw + ':' + tp)
            elif tp == 'net':
                net_set.add(kw + ':' + tp)
            elif tp == 'org.cn':
                org_cn_set.add(kw + ':' + tp)
            elif tp == 'net.cn':
                net_cn_set.add(kw + ':' + tp)
            # contrast_set.add(word)
        except Exception as e:
            print('wrong line == ', contrast_lines.index(line), e)
    if not contrast_lines:
        break

base_com_set = set()
for item in base_set:
    base_com_set.add(item + ':' + 'com')

base_cn_set = set()
for item in base_set:
    base_cn_set.add(item + ':' + 'cn')

base_com_cn_set = set()
for item in base_set:
    base_com_cn_set.add(item + ':' + 'com.cn')

base_org_set = set()
for item in base_set:
    base_org_set.add(item + ':' + 'org')

base_org_cn_set = set()
for item in base_set:
    base_org_cn_set.add(item + ':' + 'org.cn')

base_net_set = set()
for item in base_set:
    base_net_set.add(item + ':' + 'net')

base_net_cn_set = set()
for item in base_set:
    base_net_cn_set.add(item + ':' + 'net.cn')

# 做集合减法运算得出差值,确定哪些关键字没有被爬取
dif_com_set = base_com_set - com_set
dif_com_cn_set = base_com_cn_set - com_cn_set
dif_cn_set = base_cn_set - cn_set
dif_org_set = base_org_set - org_set
dif_org_cn_set = base_org_cn_set - org_cn_set
dif_net_set = base_net_set - net_set
dif_net_cn_set = base_net_cn_set - net_cn_set

# print(different_set)
# print(len(different_set))

new_com_file = open('./网域数据/lost_com_data.txt', 'w+', encoding='utf-8')
for key in dif_com_set:
    key = key.split(':')[0]
    new_com_file.write('"%s"' % key + '\n')
new_com_file.close()

new_cn_file = open('./网域数据/lost_cn_data.txt', 'w+', encoding='utf-8')
for key in dif_cn_set:
    key = key.split(':')[0]
    new_cn_file.write('"%s"' % key + '\n')
new_cn_file.close()

new_com_cn_file = open('./网域数据/lost_com_cn_data.txt', 'w+', encoding='utf-8')
for key in dif_com_cn_set:
    key = key.split(':')[0]
    new_com_cn_file.write('"%s"' % key + '\n')
new_com_cn_file.close()

new_org_file = open('./网域数据/lost_org_data.txt', 'w+', encoding='utf-8')
for key in dif_org_set:
    key = key.split(':')[0]
    new_org_file.write('"%s"' % key + '\n')
new_org_file.close()

new_org_cn_file = open('./网域数据/lost_org_cn_data.txt', 'w+', encoding='utf-8')
for key in dif_org_cn_set:
    key = key.split(':')[0]
    new_org_cn_file.write('"%s"' % key + '\n')
new_org_cn_file.close()

new_net_file = open('./网域数据/lost_net_data.txt', 'w+', encoding='utf-8')
for key in dif_net_set:
    key = key.split(':')[0]
    new_net_file.write('"%s"' % key + '\n')
new_net_file.close()

new_net_cn_file = open('./网域数据/lost_net_cn_data.txt', 'w+', encoding='utf-8')
for key in dif_net_cn_set:
    key = key.split(':')[0]
    new_net_cn_file.write('"%s"' % key + '\n')
new_net_cn_file.close()

print('finished!!!')
