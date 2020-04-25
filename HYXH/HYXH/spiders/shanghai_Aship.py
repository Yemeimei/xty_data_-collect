# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from gne import GeneralNewsExtractor
import re
import logging

from scrapy.spiders import CrawlSpider, Rule

from HYXH.items import HyxhItem
from HYXH.util_custom.tools.attachment import get_attachments, get_times


class HySpider(CrawlSpider):
    name = 'shanghai_Aship'
    allowed_domains = ['www.ssnaoe.org']
    start_urls = [
        f'http://www.ssnaoe.org/shcbyhy/node3/n6/index{x}.html'for x in range(1, 172)
    ]
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 10,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1000000000,
        'CONCURRENT_REQUESTS_PER_IP':0,
        # 下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'HYXH.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'HYXH.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'HYXH.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'HYXH.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'HYXH.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
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
        Rule(LinkExtractor(restrict_css='.liebiao a'), callback='parse_items', follow=True),
    )

    def parse_items(self, response):
        lyurl = response.url
        extractor = GeneralNewsExtractor()
        resp = response.text
        result = extractor.extract(resp, with_body_html=False)
        title = response.css('h2::text').extract_first()
        txt = result['content']
        publish_time = response.xpath('//div[@class="main2 ma clear"]/span[@class="riqi_1"][1]/text()').extract_first()
        # publish_time = response.xpath('/html/body/div[4]/span[1]/text()').extract_first()
        print('publish_time:' + str(publish_time))
        time = get_times(publish_time)
        item = HyxhItem()
        content_css = [
            '.para.ma'
        ]
        for content in content_css:
            content = ''.join(response.css(content).extract())
            if content:
                break
            if not content:
                logging.warning(f'{response.url}' + '当前url无 css 适配未提取 centent')
        item['title'] = title
        appendix, appendix_name = get_attachments(response)
        item['appendix'] = appendix
        item['source'] = '上海市船舶与海洋工程学会'
        item['website'] = '上海市船舶与海洋工程学会'
        item['link'] = lyurl
        item['appendix_name'] = appendix_name
        item['type'] = 1
        item['tags'] = ''
        item['time'] = time
        item['content'] = content
        item['txt'] = txt
        item['spider_name'] = 'shanghai_Aship'
        item['module_name'] = '行业协会'
        yield item

