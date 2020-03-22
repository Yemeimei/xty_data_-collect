# -*- coding: utf-8 -*-
import logging
import re

import scrapy
from gne import GeneralNewsExtractor

from YanB.items import YanbItem
from YanB.util_custom.tools.attachment import get_attachments, get_times
from YanB.util_custom.tools.cate import get_category



class YbWbSpider(scrapy.Spider):
    name = 'YB_wb'
    # allowed_domains = ['wwwww']
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 10,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1000000,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        # 下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'YanB.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'HY_NEWS.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'HY_NEWS.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'YanB.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'YanB.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
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
    start_urls = ['https://data.weibo.com/report/report?order=all-all-all-all-sj']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        urls = response.css(".second-list a::attr(href)").extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        item = YanbItem()
        resp = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(resp, with_body_html=False)
        title = result['title']
        txt = result['content']
        p_time = result['publish_time']
        content_css = [
            '.report-detail'
        ]
        for content in content_css:
            content = ''.join(response.css(content).extract())
            if content:
                break
            if not content:
                logging.warning(f'{response.url}' + '当前url无 css 适配未提取 centent')
        appendix, appendix_name = get_attachments(response)
        tags, _, _ = get_category(txt + title)
        industry = ''
        item['title'] = title
        item['p_time'] = get_times(str(p_time))
        item['industry'] = industry
        item['appendix'] = appendix
        item['appendix_name'] = appendix_name
        item['content'] = ''.join(content)
        item['pub'] = '微报告'
        item['ctype'] = 3
        item['website'] = '微报告'
        item['txt'] = ''.join(txt).strip()
        item['link'] = response.url
        item['spider_name'] = 'YB_wb'
        item['module_name'] = '研报'
        item['tags'] = tags
        if content:
            yield item
