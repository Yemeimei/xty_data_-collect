# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BrandItem(scrapy.Item):
    code = scrapy.Field()
    brand = scrapy.Field()
    month = scrapy.Field()
    sale_num = scrapy.Field()
    unit = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    tags = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()

class CompanyItem(scrapy.Item):
    code = scrapy.Field()
    company = scrapy.Field()
    month = scrapy.Field()
    sale_num = scrapy.Field()
    unit = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    tags = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()

class CartypeItem(scrapy.Item):
    code = scrapy.Field()
    car_type = scrapy.Field()
    month = scrapy.Field()
    sale_num = scrapy.Field()
    unit = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    tags = scrapy.Field()
    spider_name = scrapy.Field()
    module_name = scrapy.Field()