import re
import zlib

pdf = open("./a.pdf", "rb").read()
stream = re.compile(r'.*?FlateDecode.*?stream(.*?)endstream', re.S)

for s in stream.findall(pdf):
    s = s.strip('\r\n')
    try:
        print(zlib.decompress(s))
        print("")
    except:
        pass