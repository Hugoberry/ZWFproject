import re
import json

base_file = open('./交易库商标名称名录.txt', 'r+', encoding='utf-8')
base_set = set()
lines = base_file.readlines()
for line in lines:
    word = re.compile('"(.*)"').findall(line)[0]
    base_set.add(word)

contrast_file = open('./知乎话题/zh_topic_json.txt', 'r+', encoding='utf-8')
contrast_set = set()
contrast_lines = contrast_file.readlines()
for line in contrast_lines:
    try:
        word = json.loads(line, encoding='utf-8')
        word = word['kw']
        contrast_set.add(word)
    except IndexError:
        print('wrong line == ', contrast_lines.index(line))

different_set = base_set - contrast_set
print(different_set)
print(len(different_set))

new_file = open('./知乎话题/lost_data.txt', 'w+', encoding='utf-8')
for key in different_set:
    new_file.write('"%s"' % key + '\n')
new_file.close()
print('finished!!!')
