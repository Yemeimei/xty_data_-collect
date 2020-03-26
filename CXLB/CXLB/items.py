# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CXLBItem(scrapy.Item):
    main_product = scrapy.Field()
    type = scrapy.Field()
    company_name = scrapy.Field()
    unit = scrapy.Field()
    sale_num = scrapy.Field()
    product_num = scrapy.Field()
    storage_num = scrapy.Field()
    sale_ratio = scrapy.Field()
    product_ratio = scrapy.Field()
    storage_ratio = scrapy.Field()
    years = scrapy.Field()
    tags = scrapy.Field()
    appendix_name = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    create_time = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()

