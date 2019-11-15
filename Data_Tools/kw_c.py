import re

raw_file = open('tm_name.txt', 'r+', encoding='utf-8')
aim_file = open('kw_count.txt', 'w+', encoding='utf-8')
contract_file = open('所有.txt', 'r+', encoding='utf-8')

kw_set = set()
all_ls = []

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        kw = line.replace('\n', '')
        if kw:
            kw_set.add(kw)

while True:
    lines = contract_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        word = line.replace('\n', '')
        all_ls.append(word)

for kw in kw_set:
    ct = 0
    for k in all_ls:
        if re.compile(kw).findall(k):
            ct += 1
    # ct = all_ls.count(re.compile(kw).findall(all_ls)[0])
    aim_file.write(kw + '\t' + str(ct) + '\n')
    print(kw + str(ct))
    aim_file.flush()

raw_file.close()
aim_file.close()
contract_file.close()
print('finished!!!!')
