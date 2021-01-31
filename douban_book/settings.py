# -*- coding: utf-8 -*-
"""
@Time   : 2021/1/21 8:40 PM
@author : Yuan Tian
"""

REDIS_URL = 'redis://:xlib@172.16.0.138:6379/13'
MYSQL_DATABASE = 'collie'

# 16/1 -> 32/0.1
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.1
DOWNLOAD_TIMEOUT = 30

COOKIES_ENABLED = False
REDIRECT_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    'Accept-Encoding': 'gzip',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}


# DataLoss
# DOWNLOAD_FAIL_ON_DATALOSS = False

BOT_NAME = 'douban_book'

SPIDER_MODULES = ['douban_book.spiders']
NEWSPIDER_MODULE = 'douban_book.spiders'

# DFS
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

# unlimited Depth
DEPTH_LIMIT = 0
DEPTH_STATS_VERBOSE = True

# 启动Scrapy-Redis去重过滤器，取消Scrapy的去重功能
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 启用Scrapy-Redis的调度器，取消Scrapy的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Scrapy-Redis断点续爬
SCHEDULER_PERSIST = True
# 配置Redis数据库的连接，密码默认为空 redis://user:password@host:poc rert/db

# 清洗记录的爬取队列和指纹集合，重爬
# SCHEDULER_FLUSH_ON_START = True

# Mysql
MYSQL_HOST = '172.16.0.138'
# MYSQL_DATABASE = 'collie_test'
MYSQL_PORT = 3306
MYSQL_USER = 'x-lib'
MYSQL_PASSWORD = 'xlib'

# Logging
# LOG_LEVEL = "DEBUG"
LOG_LEVEL = "INFO"
from datetime import datetime
n = datetime.now().strftime('%m_%d_%H_%M_%S')
# LOG_FILE = f"./logs/{n}_error.log"

RETRY_TIMES = 2
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 407, 408, 429, 520]
HTTPERROR_ALLOWED_CODES = [302, 301, 403]    # 允许返回response到spider中处理

# 图像存储
# IMAGES_STORE = './images'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban_book (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16


# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'douban_book.middlewares.DoubanBookSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 100,
        # 'douban_book.middlewares.RandomUserAgentMiddleware': 100,
        'douban_book.middlewares.ProxyDownloaderMiddleware': 101,
        'douban_book.middlewares.DoubanBookDownloaderMiddleware': 544,
        'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,  # default已经设置
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'douban_book.pipelines.MysqlPipeline': 300,
    # 'douban_book.pipelines.ImagePipeline': 301,
    'douban_book.pipelines.DoubanPipeline': 302,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'