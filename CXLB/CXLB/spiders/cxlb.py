# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from gne import GeneralNewsExtractor
import re
import logging

from scrapy.spiders import CrawlSpider, Rule

from CXLB.items import CXLBItem
from CXLB.util_custom.tools.attachment import get_attachments, get_times


class HySpider(CrawlSpider):
    name = 'cxlb'
    allowed_domains = ['db.yaozh.com']
    start_urls = [
        f'https://db.yaozh.com/cxlb?p={x}&pageSize=20'
        for x in range(1, 77)]
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 10,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1000000000,
        'CONCURRENT_REQUESTS_PER_IP':0,
        # 下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'CXLB.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'CXLB.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'CXLB.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'CXLB.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'CXLB.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
        },
        # 调用 scrapy_splash 打开此设置
        # 'SPIDER_MIDDLEWARES': {
        #     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        # },
        # 去重/api端口
        # 'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # # 'SPLASH_URL': "http://10.8.32.122:8050/"
        # 'SPLASH_URL': "http://127.0.0.1:8050/"
    }
    # def start_requests(self):
        # pass

    def parse(self, response):
        for tr in response.css('.table.table-striped tbody tr'):
            item = CXLBItem()
            item['main_product'] = tr.xpath('./th/text()').extract_first()
            item['type'] = tr.xpath('./td[1]/text()').extract_first()
            item['company_name'] = tr.xpath('./td[2]/text()').extract_first()
            item['unit'] = tr.xpath('./td[3]/text()').extract_first()
            item['sale_num'] = tr.xpath('./td[4]/text()').extract_first()
            item['product_num'] = tr.xpath('./td[5]/text()').extract_first()
            item['storage_num'] = tr.xpath('./td[6]/text()').extract_first()
            item['sale_ratio'] = tr.xpath('./td[7]/text()').extract_first()
            item['product_ratio'] = tr.xpath('./td[8]/text()').extract_first()
            item['storage_ratio'] = tr.xpath('./td[9]/text()').extract_first()
            item['years'] = tr.xpath('./td[10]/text()').extract_first()
            item['tags'] = ''
            item['appendix_name'] = ''
            item['website'] = '药智数据'
            item['link'] = ''
            item['spider_name'] = 'cxlb'
            item['module_name'] = '产销库'

            yield item
