# Scrapy settings for ZhihuTopicRedis project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['ZhihuTopicRedis.spiders']
NEWSPIDER_MODULE = 'ZhihuTopicRedis.spiders'
ROBOTSTXT_OBEY = False

# USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    'ZhihuTopicRedis.pipelines.ZhihutopicPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1
#CONCURRENT_REQUESTS = 32
DOWNLOADER_MIDDLEWARES = {
   'ZhihuTopicRedis.middlewares.RandMiddleware': 543,
   'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
