# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XtyDataCollectItem(scrapy.Item):
    #根据入库数据构建 itme
    pub = scrapy.Field()
    p_time = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    appendix = scrapy.Field()
    symbol = scrapy.Field()
    region = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    spider_name =scrapy.Field()
    txt =scrapy.Field()
    appendix_name=scrapy.Field()
    module_name =scrapy.Field()
    city =scrapy.Field()