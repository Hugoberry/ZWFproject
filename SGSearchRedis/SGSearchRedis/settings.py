# Scrapy settings for SGSearchRedis project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['SGSearchRedis.spiders']
NEWSPIDER_MODULE = 'SGSearchRedis.spiders'
ROBOTSTXT_OBEY = False

# USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'
CONCURRENT_REQUESTS = 32
RETRY_ENABLED = True  # 重试中间件 指定关闭 默认为 True 是开启状态
RETRY_HTTP_CODES = [302]  # 指定要重试的 HTTP 状态码，其它错误会被丢弃
RETRY_TIMES = 2  # 指定重试次数
AUTOTHROTTLE_ENABLED = True  # 自动限速扩展
AUTOTHROTTLE_START_DELAY = 5.0
#  最初的下载延迟（以秒为单位）
AUTOTHROTTLE_MAX_DELAY = 60.0
#  在高延迟情况下设置的最大下载延迟（以秒为单位）
AUTOTHROTTLE_DEBUG = True
#  启用 AutoThrottle 调试模式，该模式显示收到的每个响应的统计数据，以便可以实时调节参数
AUTOTHROTTLE_TARGET_CONCURRENCY = 10
# Scrapy 应平行发送到远程网站的请求数量 将此选项设置为更高的值以增加吞吐量和远程服务器上的负载 将此选项设置为更低的值以使爬虫更保守和礼貌
# HTTPERROR_ALLOWED_CODES=[302, 500, 502, 404, 403, 503],
# DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 10
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
REDIS_HOST = '10.10.21.141'  # 也可以根据情况改成 localhost
REDIS_PORT = 6379
REDIS_PARAMS = {
    'db': 10,
}
ITEM_PIPELINES = {
    'SGSearchRedis.pipelines.SearchPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
   'SGSearchRedis.middlewares.RandMiddleware': 543,
    'SGSearchRedis.middlewares.ProcessAllExceptionMiddleware': 544,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
