raw_file = open("./cnki_detail.txt", mode="r+", encoding="utf-8")
new_file = open("./kkk.txt", mode="w+", encoding="utf-8")

k_dict = dict()

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        raw_dict = eval(line.replace("\n", ""))
        for k, v in raw_dict.items():
            if k in k_dict:
                k_dict[k] += 1
            else:
                k_dict[k] = 1

raw_file.close()

# k_ls = []
for k, v in k_dict.items():
    if v > 7000:
        # k_ls.append(k)
        new_file.write(k + "\n")

# raw_file = open("./cnki_detail.txt", mode="r+", encoding="utf-8")
# while True:
#     lines = raw_file.readlines(4096)
#     if not lines:
#         break
#     for line in lines:
#         for k in k_ls:
#             line = line.replace("'%s'" % k, '"%s"' % k)
#         line = line.replace("'", "’")
#         new_file.write(line)

# raw_file.close()

new_file.close()
