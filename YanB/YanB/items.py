# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YanbItem(scrapy.Item):
    title = scrapy.Field()
    p_time = scrapy.Field()
    industry = scrapy.Field()
    content = scrapy.Field()
    appendix = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    ctype = scrapy.Field()
    pub = scrapy.Field()
    tags = scrapy.Field()
    appendix_name = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()