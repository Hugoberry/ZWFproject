# import json

# s = '坤焰	{19:3,3:1,35:4,5:1,24:1,25:1,42:1,43:1,30:3,31:1}'
s = 'a	{}'
info = s.split('\t')
word = info[0]
new_ls = info[1][1:-1].split(',')
# print(new_ls)
new_dict = {}
for l in new_ls:
    if not l:
        pass
    else:
        new_dict[l.split(':')[0]] = l.split(':')[1]
# print(new_dict)
for i in range(1, 46):
    if str(i) not in new_dict:
        new_dict[str(i)] = '0'
# print(new_dict)
nums_ls = [new_dict[str(i)] for i in range(1, 46)]
print(str(nums_ls)[1:-1].replace(',', '\t').replace("'", ''))

# data = json.loads(info[1], encoding='utf-8')
# print(data)

# data = info[1].replace('{', '').replace('}', '')
# if data:
#     data = data.split(',')
#
# print(word, '=======', data)
# sum_nums = 0
# for dt in data:
#     data_info = dt.split(':')
#     sum_nums += int(data_info[1])
# print(sum_nums)
# data_text = info[1].replace('{', '').replace('}', '').replace(',', '\t').replace(':', '\t')
# if data_text:
#     print(word + '\t' + data_text + '\t' + str(sum_nums))
# else:
#     print(word + '\t' + str(sum_nums))
