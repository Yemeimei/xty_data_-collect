# -*- coding: utf-8 -*-
import scrapy
import logging
from HAIGUAN.items import HaiguanItem
from HAIGUAN.util_custom.tools.attachment import get_attachments, get_times

class HgzsTjybSpider(scrapy.Spider):
    name = 'HGZS_TJYB'
    # allowed_domains = ['http://www.customs.gov.cn/customs/302249/302274/302277/index.html']
    start_urls = ['http://www.customs.gov.cn/customs/302249/302274/302277/index.html']

    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 10,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        # 下载暂停
        'DOWNLOAD_DELAY': 2,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'HAIGUAN.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'investment_news.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'HAIGUAN.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'HAIGUAN.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'HAIGUAN.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
        },
        # 调用 scrapy_splash 打开此设置
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        # 去重/api端口
        # 'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # # 'SPLASH_URL': "http://10.8.32.122:8050/"
        'SPLASH_URL': "http://47.106.239.73:8050/"
    }

    def parse(self, response):
        for href in response.css('td a.blue::attr(href)').extract():
            url = response.urljoin(href).strip()
            if (url.endswith('.html') or url.endswith('.htm')) and url.startswith('http://') and (url != response.url):
                yield scrapy.Request(url, callback=self.parse_item, meta=response.meta, dont_filter=True)

    def parse_item(self, response):
        try:
            item = HaiguanItem()
            item['title'] = response.css('title::text').extract_first()
            item['content'] = response.css('#easysiteText').extract_first()
            item['time'] = get_times(response.css('.easysite-news-describe::text').extract_first())
            item['website'] = '中华人民共和国海关总署-统计月报'
            item['link'] = response.url
            item['type'] = '2'
            item['source'] = '中华人民共和国海关总署'
            item['txt'] = ''.join(response.css('#easysiteText *::text').extract())
            item['module_name'] = '中华人民共和国海关总署-统计月报'
            item['spider_name'] = 'HGZS_TJYB'
            print(
                "===========================>crawled one item" +
                response.request.url)
        except Exception as e:
            logging.error(
                self.name +
                " in parse_item: url=" +
                response.request.url +
                ", exception=" +
                e.__str__())
            logging.exception(e)
        yield item
