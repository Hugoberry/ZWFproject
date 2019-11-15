from scrapy import cmdline
import sys

num = sys.argv[1]
# relation
# cmdline.execute('scrapy runspider EUIPO_REDIS/spiders/ipo_relation.py'.split())
# # document
# cmdline.execute('scrapy runspider EUIPO_REDIS/spiders/ipo_document.py'.split())
# # img
# cmdline.execute('scrapy runspider EUIPO_REDIS/spiders/ipo_img.py'.split())
# # communications
cmdline.execute('scrapy runspider EUIPO_REDIS/spiders/ipo_communications.py'.split())
# # timeline
# cmdline.execute('scrapy runspider EUIPO_REDIS/spiders/ipo_timeline.py'.split())
