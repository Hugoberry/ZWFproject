import json

raw_file = open("./unsp.txt", mode="r+", encoding="utf-8")
new_file = open("./detail_r.txt", mode="w+", encoding="utf-8")
w_file = open("./detail_w.txt", mode="w+", encoding="utf-8")
empty_word = '""'
kw_ls = ["link", "申请号", "申请日", "公开号", "公开日", "申请人", "地址", "共同申请人", "发明人", "国际申请",
         "国际公布", "进入国家日期", "专利代理机构", "代理人", "分案原申请号", "国省代码", "摘要", "主权项", "页数",
         "主分类号", "专利分类号"]
new_file.write("\t".join(kw_ls) + "\n")

while True:
    lines = raw_file.readlines(4096)
    if not lines:
        break
    for line in lines:
        try:
            raw_dict = json.loads(line.replace("\n", ""))
            l_str = []
            for kw in kw_ls:
                if kw in raw_dict:
                    l_str.append(raw_dict[kw].replace("\r", "").replace("\n", ""))
                else:
                    l_str.append(empty_word)
            new_file.write("\t".join(l_str) + "\n")
        except Exception as e:
            print(e)
            w_file.write(line)

w_file.close()
raw_file.close()
new_file.close()
