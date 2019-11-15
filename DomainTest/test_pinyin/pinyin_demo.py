from xpinyin import Pinyin

p = Pinyin().get_pinyin('啊啊p啊')
print(p.replace('-', '').replace(' ', '').lower())
