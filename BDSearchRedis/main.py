from scrapy import cmdline
import sys

num = sys.argv[1]

cmdline.execute('scrapy runspider ./BDSearchRedis/spiders/bd_search.py'.split())
