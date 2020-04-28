# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from gne import GeneralNewsExtractor
import re
import logging

from scrapy.spiders import CrawlSpider, Rule

from SHQC.items import BrandItem
from SHQC.items import CompanyItem
from SHQC.items import CartypeItem
from SHQC.util_custom.tools.attachment import get_attachments, get_times


class HySpider(CrawlSpider):
    name = 'shqc'
    allowed_domains = ['db.auto.sohu.com']
    start_urls = ['http://db.auto.sohu.com/cxdata/iframe.html']
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 10,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1000000000,
        'CONCURRENT_REQUESTS_PER_IP':0,
        # 下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'SHQC.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'SHQC.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'SHQC.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'SHQC.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'SHQC.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
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
        for th in response.xpath('//*[@id="sortTable"]/tbody/tr[1]/th'):
            dates = th.xpath('./span/text()').extract_first()
            index = 2
            if dates != '品牌':
                index = index + 1
                for tr in response.xpath('//*[@id="sortTable"]/tbody/tr[position()>1]'):
                    item = BrandItem()
                    item['code'] = tr.xpath('./td[1]/text()').extract_first()
                    item['brand'] = tr.xpath('./td[2]/a/text()').extract_first()
                    item['month'] = dates
                    item['sale_num'] = tr.xpath('./td['+str(index)+']/text()').extract_first()
                    item['unit'] = '辆'
                    item['website'] = '搜狐汽车'
                    item['link'] = response.urljoin(tr.xpath('./td[2]/a/@href').extract_first())
                    item['tags'] = ''
                    item['spider_name'] = 'brand'
                    item['module_name'] = '汽车产销-品牌'
                    data = {}
                    data['type'] = 'brand'
                    data['item'] = item
                    yield data

        for th in response.xpath('//*[@id="sortTable2"]/tbody/tr[1]/th'):
            dates = th.xpath('./span/text()').extract_first()
            index = 2
            if dates != '企业':
                index = index + 1
                for tr in response.xpath('//*[@id="sortTable2"]/tbody/tr[position()>1]'):
                    item = CompanyItem()
                    item['code'] = tr.xpath('./td[1]/text()').extract_first()
                    item['company'] = tr.xpath('./td[2]/a/text()').extract_first()
                    item['month'] = dates
                    item['sale_num'] = tr.xpath('./td[' + str(index) + ']/text()').extract_first()
                    item['unit'] = '辆'
                    item['website'] = '搜狐汽车'
                    item['link'] = response.urljoin(tr.xpath('./td[2]/a/@href').extract_first())
                    item['tags'] = ''
                    item['spider_name'] = 'company'
                    item['module_name'] = '汽车产销-企业'
                    data = {}
                    data['type'] = 'company'
                    data['item'] = item
                    yield data

        for th in response.xpath('//*[@id="sortTable3"]/tbody/tr[1]/th'):
            dates = th.xpath('./span/text()').extract_first()
            index = 2
            if dates != '车型':
                index = index + 1
                for tr in response.xpath('//*[@id="sortTable3"]/tbody/tr[position()>1]'):
                    item = CartypeItem()
                    item['code'] = tr.xpath('./td[1]/text()').extract_first()
                    item['car_type'] = tr.xpath('./td[2]/a/text()').extract_first()
                    item['month'] = dates
                    item['sale_num'] = tr.xpath('./td[' + str(index) + ']/text()').extract_first()
                    item['unit'] = '辆'
                    item['website'] = '搜狐汽车'
                    item['link'] = response.urljoin(tr.xpath('./td[2]/a/@href').extract_first())
                    item['tags'] = ''
                    item['spider_name'] = 'car_type'
                    item['module_name'] = '汽车产销-车型'
                    data = {}
                    data['type'] = 'car_type'
                    data['item'] = item
                    yield data
