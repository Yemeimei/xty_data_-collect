# -*- coding: utf-8 -*-



import scrapy
import json

from YanB.items import YanbItem
from YanB.util_custom.tools.cate import get_category


class YbZscySpider(scrapy.Spider):
    name = 'YB_ZSCY'
    # allowed_domains = ['http://wk.askci.com/ListTable/?pageNum=1']
    # start_urls = ['http://http://wk.askci.com/ListTable/?pageNum=1/']
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

    def start_requests(self):
        for x in range(1,30):
            url = f'https://wk.askci.com/ListTable/GetList?keyword=&bookName=&tradeId=&typeId=&tagName=&publisher=&page={x}&limit=30'
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        item = YanbItem()
        js =json.loads(response.text)

        for html in js['data']:
            item['title'] = html['BookName']
            item['p_time'] = html['StrBookPublishDate']
            item['industry'] = ''
            item['appendix'] = ''
            item['appendix_name'] = ''
            item['content'] =  html['ReadUrl']
            item['pub'] = 'YB_ZSCY'
            item['ctype'] = 3
            item['website'] = 'YB_ZSCY'
            item['txt'] = ''
            item['link'] = response.url
            item['spider_name'] = 'YB_ZSCY'
            item['module_name'] = '研报'
            tags, _, _ = get_category(item['title'])
            item['tags'] = tags
            yield item