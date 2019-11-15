file = open('./cnki_kw.txt', mode='r+', encoding='utf-8')
while True:
    lines = file.readlines(4096)
    if not lines:
        break
    for line in lines:
        kw = line.replace("\n", "")
        print(kw)
