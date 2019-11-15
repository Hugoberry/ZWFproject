note = '''
    # 这个程序是为了检测未怕去到的数据,即未检测到的数据文件
    # lost_set = all_set - already_set
    # 这个集合得到的是没有怕去到的数据
    # 得到的contract.txt是需要重新爬取的数据
'''

raw_file = open('./retest_domain.txt', 'r+', encoding='utf-8')
already_file = open('./already.txt', 'r+', encoding='utf-8')
contract_file = open('./contract.txt', 'w+', encoding='utf-8')

# 设置集合
all_set = set()
already_set = set()

# 读取文件
while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        all_set.add(line.strip())

while True:
    lines = already_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        already_set.add(line.strip())

lost_set = all_set - already_set

for lo in lost_set:
    contract_file.write(lo + '\n')

raw_file.close()
already_file.close()
contract_file.close()
