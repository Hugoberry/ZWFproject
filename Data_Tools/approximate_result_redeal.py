raw_file = open('./近似结果', 'r+', encoding='utf-8')
new_file = open('./approximate_result.txt', 'w+', encoding='utf-8')

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        info = line.split('\t')
        word = info[0]
        data = info[1].replace('{', '').replace('}', '')
        if data:
            data = data.split(',')
        sum_nums = 0
        for dt in data:
            data_info = dt.replace('\n', '').split(':')
            if data_info[0]:
                sum_nums += int(data_info[1])
        data_text = info[1].replace('{', '').replace('}', '').replace(',', '\t').replace(':', '\t').replace('\n', '')
        if data_text:
            new_file.write(word + '\t' + data_text + '\t' + str(sum_nums) + '\n')
        else:
            new_file.write(word + '\n')

raw_file.close()
new_file.close()
print('finished!!!')
