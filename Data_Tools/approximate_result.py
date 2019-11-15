raw_file = open('./spider_kw.txt', 'r+', encoding='utf-8')
new_file = open('./spider_data.txt', 'w+', encoding='utf-8')
new_file.write('key\t1\t2\t3\t4\t5\t6\t7\t8\t9\t10\t11\t12\t13\t14\t15\t16\t17\t18\t19\t20\t21\t22\t23\t24\t25'
               '\t26\t27\t28\t29\t30\t31\t32\t33\t34\t35\t36\t37\t38\t39\t40\t41\t42\t43\t44\t45\tsum\n')

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        info = line.replace('\n', '').split('\t')
        word = info[0]

        new_ls = info[1][1:-1].split(',')
        new_dict = {}
        for l in new_ls:
            if not l:
                pass
            else:
                new_dict[l.split(':')[0]] = l.split(':')[1]
        for i in range(1, 46):
            if str(i) not in new_dict:
                new_dict[str(i)] = '0'
        nums_ls = [new_dict[str(i)] for i in range(1, 46)]

        data = info[1].replace('{', '').replace('}', '')
        if data:
            data = data.split(',')
        sum_nums = 0
        for dt in data:
            data_info = dt.replace('\n', '').split(':')
            if data_info[0]:
                sum_nums += int(data_info[1])

        new_file.write(word + '\t' + str(nums_ls)[1:-1].replace(',', '\t').replace("'", '') + '\t' + str(sum_nums) + '\n')

        # # data_text = info[1].replace('{', '').replace('}', '').replace(',', '\t').replace(':', '\t').replace('\n', '')
        # data_text = info[1].replace('{', '').replace('}', '').replace('\n', '').split(',')
        # for dt in data_text:
        #     type_no = dt.split(':')[0]
        #     if int(type_no) in range(1, 46):
        #         pass
        # if data_text:
        #     new_file.write(word + '\t' + data_text + '\t' + str(sum_nums) + '\n')
        # else:
        #     new_file.write(word + '\n')

raw_file.close()
new_file.close()
print('finished!!!')
