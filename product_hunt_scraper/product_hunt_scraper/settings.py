BOT_NAME = "product_hunt_scraper"

SPIDER_MODULES = ["product_hunt_scraper.spiders"]
NEWSPIDER_MODULE = "product_hunt_scraper.spiders"

CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 5

CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16


AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0


# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"


RETRY_ENABLED = True
RETRY_TIMES = 2

LOG_LEVEL = 'INFO'


REDIS_URL = 'redis://:Y12h12p12@localhost:6379'  # Use your Redis server details
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True

REDIS_PARAMS = {
    'password': 'Y12h12p12',
}


