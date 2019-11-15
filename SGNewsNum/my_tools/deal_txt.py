import re
import os

if not os.path.exists('./aim/'):
    os.makedirs('./aim/')
aim_len = 100
source_file = open('./交易库商标名称名录.txt', 'r+', encoding='utf-8')
lines = source_file.readlines()
kw_ls = []
for line in lines:
    kw = re.compile('\"(.*)\"').findall(line)[0]
    kw_ls.append(kw)
line_len = int(len(kw_ls) / aim_len) + 1
for i in range(line_len):
    aim_file = open('./aim/aim%s.txt' % str(i + 1), 'w+', encoding='utf-8')
    for k in kw_ls[aim_len * i:aim_len * (i + 1)]:
        aim_file.write(k + '\n')
    aim_file.close()
print('finish!!!')
