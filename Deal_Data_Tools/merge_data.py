raw_file = open('./url_confirm.txt', 'r+', encoding='utf-8')
raw_file_other = open('./url_confirm1.txt', 'r+', encoding='utf-8')
new_file = open('./sum_confirm.txt', 'w+', encoding='utf-8')

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break

    for line in lines:
        new_file.write(line)

while True:
    lines = raw_file_other.readlines(4096)
    if not lines:
        break

    for line in lines:
        new_file.write(line)

print('finished!!!')
raw_file.close()
raw_file_other.close()
new_file.close()
