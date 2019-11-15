from scrapy import cmdline
import sys

num = sys.argv[1]
cmdline.execute('scrapy runspider Game9/spiders/game.py'.split())
