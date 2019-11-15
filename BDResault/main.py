from scrapy import cmdline
import sys

num = sys.argv[1]
cmdline.execute('scrapy runspider BDResult/spiders/baidu.py'.split())
