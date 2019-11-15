import json
import re

# 这个程序是为了检测重复爬取的网页数据, 并把这些重复的数据重写
# 打开重复的文件
repeat_file = open('./contract.txt', 'r+', encoding='utf-8')
# 打开所有的数据文件
raw_file = open('./sum_confirm.txt', 'r+', encoding='utf-8')
# 打开需要处理数据的目标文件(新创建的)
aim_file = open('./aim_data.txt', 'w+', encoding='utf-8')

# 逻辑
# 读出重复文件的网址, 对比和已经爬到数据的重复点, 替换关键字即可

# 规定容器
line_dict = {}

while True:
    lines = repeat_file.readlines(4096)
    for line in lines:
        (value, key) = re.compile(r'(.*)\t(.*)').findall(line)[0]
        line_dict[key] = value
    if not lines:
        break

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        json_line = json.loads(line, encoding='utf-8')
        if json_line['domain'] in line_dict:
            json_line['kw'] = line_dict[json_line['domain']]
            aim_file.write(json.dumps(json_line, ensure_ascii=False) + '\n')

print('finished!!!')
repeat_file.close()
raw_file.close()
aim_file.close()
