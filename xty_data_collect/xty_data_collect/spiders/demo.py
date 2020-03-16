# -*- coding: utf-8 -*-
import scrapy

from xty_data_collect.xty_data_collect.items import XtyDataCollectItem


class DemoSpider(scrapy.Spider):
    name = 'demo'#爬虫名称
    # allowed_domains = ['']#限制提取域名  注释掉
    start_urls = ['http://neimenggu.chinatax.gov.cn/zxfb/index_1.html']# 开始 url

    def start_requests(self,response): #构造请求 url 此函数调用时  [start_urls} 失效
        for url in response.css('.snewslist a::attr(href)').extract():
            yield scrapy.Request(url, callback=self.parse, dont_filter=True) # callback传参 , dont_filter#scrapy 去重中间件建议打开避免报错

    def parse(self, response):
        item =XtyDataCollectItem()
        title = response.css("#djhjianj > p ::text").extract()
        item['title'] =title
        yield item

