new_file = open('./sum_data.txt', mode='w+', encoding='utf-8')
for i in range(6):
    raw_file = open('./part-0000%s' % str(i), mode='r+', encoding='utf-8')
    lines = raw_file.readlines()
    for line in lines:
        new_file.write(line)
    raw_file.close()
new_file.close()
