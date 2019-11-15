import pandas

file = pandas.read_csv('tm_name.txt', sep='\r\n', encoding='utf-8', engine='python')
print(file.count())
