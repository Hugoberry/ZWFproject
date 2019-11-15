# Scrapy settings for LieBiao_Redis project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['LieBiao_Redis.spiders']
NEWSPIDER_MODULE = 'LieBiao_Redis.spiders'

# USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'
ROBOTSTXT_OBEY = False

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    'LieBiao_Redis.pipelines.LiebiaoPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

DOWNLOADER_MIDDLEWARES = {
    'LieBiao_Redis.middlewares.RandMiddleWare': 543,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

REDIS_HOST = '127.0.0.1'  # 也可以根据情况改成 localhost
REDIS_PORT = 6379
REDIS_PARAMS = {
    'db': 15,
}
CONCURRENT_REQUESTS = 1
DOWNLOAD_TIMEOUT = 8
AUTOTHROTTLE_TARGET_CONCURRENCY = 8
RETRY_ENABLED = True  # 重试中间件 指定关闭 默认为 True 是开启状态
RETRY_TIMES = 5  # 指定重试次数
AUTOTHROTTLE_ENABLED = True  # 自动限速扩展
AUTOTHROTTLE_START_DELAY = 5.0
#  最初的下载延迟（以秒为单位）
AUTOTHROTTLE_MAX_DELAY = 60.0
#  在高延迟情况下设置的最大下载延迟（以秒为单位）
AUTOTHROTTLE_DEBUG = True
#  启用 AutoThrottle 调试模式，该模式显示收到的每个响应的统计数据，以便可以实时调节参数
