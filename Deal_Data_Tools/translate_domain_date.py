new_file = open('./domain_sum.txt', 'w+', encoding='utf-8')
raw_file = open('./sum_domain.txt', 'r+', encoding='utf-8')
raw_file_other = open('./com.txt', 'r+', encoding='utf-8')

while True:
    lines = raw_file.readlines(4096)
    for line in lines:
        new_file.write(line)
    if not lines:
        break

while True:
    lines = raw_file_other.readlines(4096)
    for line in lines:
        new_file.write(line)
    if not lines:
        break

print('finished!!!')
raw_file.close()
raw_file_other.close()
new_file.close()
