# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HyNewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    appendix = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    tags = scrapy.Field()
    type = scrapy.Field()
    create_time = scrapy.Field()
    appendix_name = scrapy.Field()
    txt = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()

