# -*- coding: utf-8 -*-

# Scrapy settings for xty_data_collect project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xty_data_collect'

SPIDER_MODULES = ['xty_data_collect.spiders']
NEWSPIDER_MODULE = 'xty_data_collect.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xty_data_collect (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# MYSQL_HOST = '10.8.32.125'
# MYSQL_PASSWORD = 'Admin123!'
# MYSQL_USER = 'root'
# MYSQL_DB = 'engineering-brain'
# MYSQL_CHRSET = 'utf8'

# MYSQL_HOST = '127.0.0.1'
# MYSQL_PASSWORD = 'yeyang112114'
# MYSQL_USER = 'root'
# MYSQL_DB = 'engineering-brain'
# MYSQL_CHRSET = 'utf8'

MYSQL_HOST = 'rm-8vbif49m6k7l651e5fo.mysql.zhangbei.rds.aliyuncs.com'
MYSQL_PASSWORD = 'Liqin1988'
MYSQL_USER = 'root'
MYSQL_DB = 'python'
MYSQL_PORT = 3306
MYSQL_CHRSET = 'utf8'
# LOG_LEVEL = 'INFO'
