raw_file = open('./前后包含结果', 'r+', encoding='utf-8')
check_file = open('./交易库商标名称名录.txt', 'r+', encoding='utf-8')
new_file = open('./spider_kw.txt', 'w+', encoding='utf-8')

check_set = set()

while True:
    lines = check_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        word = line.replace('"', '').replace('\n', '')
        check_set.add(word)

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        if line.split('\t')[0] in check_set:
            new_file.write(line)

raw_file.close()
check_file.close()
new_file.close()
print('finished!!!')
