from scrapy import cmdline
from sys import argv

num = argv[1]
cmdline.execute('scrapy runspider ./DomainRedis/spiders/net_demo.py'.split())
