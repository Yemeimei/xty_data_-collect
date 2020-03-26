# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from gne import GeneralNewsExtractor
import re
import logging

from scrapy.spiders import CrawlSpider, Rule

from TRUCK.items import TRUCKItem
from TRUCK.util_custom.tools.attachment import get_attachments, get_times


class HySpider(CrawlSpider):
    name = 'ZGKCW'
    allowed_domains = ['www.chinatruck.org']
    start_urls = [
        f'http://www.chinatruck.org/research/{x}.html'
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
            'TRUCK.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'TRUCK.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'TRUCK.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'TRUCK.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'TRUCK.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
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

    rules = (
        Rule(LinkExtractor(restrict_css='.details a'), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        extractor = GeneralNewsExtractor()
        resp = response.text
        result = extractor.extract(resp, with_body_html=False)

        title = result['title']
        publish_time = result['publish_time']
        time = get_times(publish_time)
        item = TRUCKItem()
        content_css = [
            '.details'
        ]
        lyurl = response.url
        for content in content_css:
            content = ''.join(response.css(content).extract())
            if content:
                break
            if not content:
                logging.warning(f'{response.url}' + '当前url无 css 适配未提取 centent')
        item['title'] = title
        appendix, appendix_name = get_attachments(response)
        item['source'] = '中国卡车网'
        item['website'] =  '中国卡车网'
        item['link'] = lyurl
        item['type'] = 1
        item['time'] = time
        item['content'] = content
        item['spider_name'] = 'ZGKCW'
        item['module_name'] = '产销库'
        yield item
