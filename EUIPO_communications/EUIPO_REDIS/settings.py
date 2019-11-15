# Scrapy settings for EUIPO_REDIS project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['EUIPO_REDIS.spiders']
NEWSPIDER_MODULE = 'EUIPO_REDIS.spiders'

# USER_AGENT = 'scrapy-redis (+https://github.com/rolando/scrapy-redis)'

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    'EUIPO_REDIS.pipelines.EuipoPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1
DOWNLOADER_MIDDLEWARES = {
    'EUIPO_REDIS.middlewares.RandMiddleware': 543,
    'EUIPO_REDIS.middlewares.ProcessAllExceptionMiddleware': 544,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
}
ROBOTSTXT_OBEY = False

REDIS_HOST = '10.0.7.6'  # 也可以根据情况改成 localhost
# REDIS_HOST = '40.73.36.3'  # 也可以根据情况改成 localhost
REDIS_PORT = 6667
REDIS_PARAMS = {
    'db': 15,
    'password': 'quandashi2018',
}
CONCURRENT_REQUESTS = 1
DOWNLOAD_TIMEOUT = 30
AUTOTHROTTLE_TARGET_CONCURRENCY = 1
RETRY_ENABLED = False  # 重试中间件 指定关闭 默认为 True 是开启状态
RETRY_TIMES = 3  # 指定重试次数
AUTOTHROTTLE_ENABLED = True  # 自动限速扩展
AUTOTHROTTLE_START_DELAY = 5.0
#  最初的下载延迟（以秒为单位）
AUTOTHROTTLE_MAX_DELAY = 60.0
#  在高延迟情况下设置的最大下载延迟（以秒为单位）
AUTOTHROTTLE_DEBUG = True
#  启用 AutoThrottle 调试模式，该模式显示收到的每个响应的统计数据，以便可以实时调节参数
REDIRECT_ENABLED = False

MYEXT_ENABLED = True  # 开启扩展
IDLE_NUMBER = 360  # 配置空闲持续时间单位为 360个 ，一个时间单位为5s
# 在 EXTENSIONS 配置，激活扩展
EXTENSIONS = {
            'EUIPO_REDIS.extensions.RedisSpiderSmartIdleClosedExensions': 500,
        }
