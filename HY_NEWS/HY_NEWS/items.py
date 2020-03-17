# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HyNewsItem(scrapy.Item):
    title = scrapy.Field()
    p_time = scrapy.Field()
    appendix = scrapy.Field()
    content = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    cate = scrapy.Field()
    code = scrapy.Field()
    region = scrapy.Field()
    txt = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()

