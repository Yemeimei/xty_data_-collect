# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class HyIdcSpider(CrawlSpider):
    name = 'HY_IDC'
    allowed_domains = ['http://www.idcun.com/plus/list.php?tid=6&TotalResult=10232&PageNo=1']
    start_urls = ['http://http://www.idcun.com/plus/list.php?tid=6&TotalResult=10232&PageNo=1/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        return item
