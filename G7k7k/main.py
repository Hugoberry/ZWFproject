from scrapy import cmdline
import sys

num = sys.argv[1]
cmdline.execute('scrapy runspider G7k7k/spiders/g7k.py'.split())
