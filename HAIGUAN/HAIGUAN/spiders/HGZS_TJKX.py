# -*- coding: utf-8 -*-
import scrapy


class HgzsTjkxSpider(scrapy.Spider):
    name = 'HGZS_TJKX'
    allowed_domains = ['http://www.customs.gov.cn/customs/302249/302274/302275/index.html']
    start_urls = ['http://http://www.customs.gov.cn/customs/302249/302274/302275/index.html/']

    def parse(self, response):
        pass
