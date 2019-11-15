from scrapy import cmdline
import sys

num = sys.argv[1]
cmdline.execute('scrapy runspider YouXia/spiders/youxia.py'.split())
# cmdline.execute('scrapy runspider YouXia/spiders/youxia_download.py'.split())
