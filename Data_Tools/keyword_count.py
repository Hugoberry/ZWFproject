raw_file = open('tm_name.txt', 'r+', encoding='utf-8')
aim_file = open('kw_count.txt', 'w+', encoding='utf-8')

kw_set = set()


def get_count(kw):
    with open('所有.txt', 'r+', encoding='utf-8') as contract_file:
        nums = 0
        while True:
            lines = contract_file.readlines(4096)
            if not lines:
                print(kw, nums)
                return nums
            for line in lines:
                if kw in line:
                    nums += 1


while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        kw = line.replace('\n', '')
        if kw:
            kw_set.add(kw)

for kw in kw_set:
    ct = get_count(kw)
    aim_file.write(kw + '\t' + str(ct) + '\n')
    aim_file.flush()

raw_file.close()
aim_file.close()
print('finished!!!!')
