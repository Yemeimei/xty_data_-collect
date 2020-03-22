# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HaiguanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    type = scrapy.Field()
    source = scrapy.Field()
    create_time = scrapy.Field()
    txt = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()
