from scrapy import cmdline
from sys import argv

num = argv[1]
# 'scrapy runspider ./KWIndexRedis/spiders/kw_index.py'.split()
cmdline.execute('scrapy runspider ./DomainRedis/spiders/domain.py'.split())
