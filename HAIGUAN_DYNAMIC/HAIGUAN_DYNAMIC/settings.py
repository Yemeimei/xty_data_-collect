# -*- coding: utf-8 -*-

# Scrapy settings for HAIGUAN project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'HAIGUAN_DYNAMIC'

SPIDER_MODULES = ['HAIGUAN_DYNAMIC.spiders']
NEWSPIDER_MODULE = 'HAIGUAN_DYNAMIC.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'HAIGUAN (+http://www.yourdomain.com)'

MYSQL_HOST = '10.8.32.156'
MYSQL_PASSWORD = 'zw123456'
MYSQL_USER = 'root'
MYSQL_DB = 'engineering-brain'
MYSQL_CHRSET = 'utf8'
MYSQL_PORT = 3361
LOG_LEVEL = 'INFO'

# MYSQL_HOST = '127.0.0.1'
# MYSQL_PASSWORD = 'yeyang112114'
# MYSQL_USER = 'root'
# MYSQL_DB = 'engineering-brain'
# MYSQL_CHRSET = 'utf8'

# MYSQL_HOST = 'rm-8vbif49m6k7l651e5fo.mysql.zhangbei.rds.aliyuncs.com'
# MYSQL_PASSWORD = 'Liqin1988'
# MYSQL_USER = 'root'
# MYSQL_DB = 'python'
# MYSQL_CHRSET = 'utf8'
# MYSQL_PORT = 3306
