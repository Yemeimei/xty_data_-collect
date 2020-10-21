# -*- coding: utf-8 -*-
import logging

import scrapy
from gne import GeneralNewsExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from HY_NEWS.items import HyNewsItem
from HY_NEWS.util_custom.tools.attachment import get_times


class SYZXSpider(CrawlSpider):
    name = 'HY_SYZX'
    # allowed_domains = ['www.asianmetal.cn']
    # start_urls = ['http://www.asianmetal.cn/news/getMoreProNews.am?productTwoID=14&jspBarNewsType=allTrend']
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 5,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1000000,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        # 下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'HY_NEWS.pipelines.MysqlTwistedPipeline': 600,
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
            'HY_NEWS.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'HY_NEWS.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
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
    def start_requests(self):
        for i in range(2519):
            urls = 'http://www.chinaoilonline.com/article.do?method=toArticleListByType2ByTypeidList&p1=15&p1=16&p1=17&p1=18&pageNo=' + str(i+1) + '&pageSize=22&pid=2&subLanmuId=2&rightshow=&typeid=23&titleLength=30'
            yield scrapy.Request(urls, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for d in response.css('.zxwk_li li'):
            url = d.css('.zxwk_mian_glywh_a::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(url), callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        item = HyNewsItem()
        resp = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(resp, with_body_html=False)
        title = response.css('#zxwk_left_1 h2::text').extract_first()
        txt = result['content']
        p_time = result['publish_time']
        lyurl = response.url
        lyname = '石油在线'
        content_css = [
            '#zxwk_left_1',
        ]
        for content in content_css:
            content = ''.join(response.css(content).extract())
            if content:
                break
            if not content:
                logging.warning(f'{response.url}' + '当前url无 css 适配未提取 centent')
        item['title'] = title
        item['txt'] = txt
        item['p_time'] = get_times(p_time)
        item['content'] = content
        item['spider_name'] = 'HY_SYZX'
        item['module_name'] = '石油在线'
        item['cate'] = '石油'
        item['region'] = ''
        item['code'] = ''
        item['link'] = lyurl
        item['website'] = lyname
        if content:
            yield item
