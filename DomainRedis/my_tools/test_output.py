from xpinyin import Pinyin

file = open('./lost_net_data.txt', 'r+', encoding='utf-8')
lines = file.readlines()
for line in lines:
    word = line.replace('"', '')
    kw_pinyin = Pinyin().get_pinyin(word).replace('-', '').replace(' ', '').replace('.', '').replace('·', '').replace(' ', '').replace(';', '').lower()
    print(kw_pinyin)
