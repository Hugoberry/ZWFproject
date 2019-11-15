from scrapy import cmdline
import sys

num = sys.argv[1]

cmdline.execute('scrapy runspider AppleAPPRedis/spiders/apple.py'.split())
