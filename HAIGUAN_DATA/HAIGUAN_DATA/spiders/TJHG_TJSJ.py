# -*- coding: utf-8 -*-
import scrapy
import logging
from HAIGUAN_DATA.items import HaiguanDataItem
from HAIGUAN_DATA.util_custom.tools.attachment import get_attachments, get_times
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class TjhgTjsjSpider(CrawlSpider):
    name = 'TJHG_TJSJ'
    allowed_domains = ['tianjin.customs.gov.cn']
    start_urls = [
        f'http://tianjin.customs.gov.cn/eportal/ui?pageId=427911&currentPage={x}&moduleId=de85e65757644e1f81191ab4cae200ca&staticRequest=yes' for x in range(1, 34)
    ]
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 10,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1000000000,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        # 下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'HAIGUAN_DATA.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'HAIGUAN_DATA.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'HAIGUAN_DATA.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'HAIGUAN_DATA.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'HAIGUAN_DATA.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
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

    rules = (
        Rule(LinkExtractor(restrict_css='.conList_ul a'), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        try:
            item = HaiguanDataItem()
            item['title'] = response.css('title::text').extract_first()
            item['time'] = get_times(
                response.css('.easysite-news-describe::text').extract_first())
            item['content'] = response.css('#easysiteText').extract_first()
            appendix, appendix_name = get_attachments(response)
            item['appendix'] = appendix
            item['appendix_name'] = appendix_name
            item['name'] = '中华人民共和国天津海关'
            item['website'] = '中华人民共和国天津海关-统计数据'
            item['link'] = response.url
            item['txt'] = ''.join(
                response.css('#easysiteText *::text').extract())
            item['module_name'] = '中华人民共和国天津海关-统计数据'
            item['spider_name'] = 'TJHG_TJSJ'
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
