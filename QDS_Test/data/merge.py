# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 15:56
# @Author  : lijiawei
# @Email   : lijiawei@quandashi.com
# @FileName: test.py
# @Software: PyCharm
# @Blog    : https://blog.csdn.net/flower_drop

fa = open('famousTM_1.txt')
a = fa.readlines()
fa.close()
fb = open('famousTrandMark.txt')
b = fb.readlines()
fb.close()
fc = open('phLocaltionTM.txt')
c = fc.readlines()
fc.close()
d = [i for i in a if i in b if i in c]
fd = open('famousTM_3.txt', 'w')
fd.writelines(d)
fd.close()
