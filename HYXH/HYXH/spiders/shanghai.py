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
    name = 'shanghai'
    # allowed_domains = ['www.smianet.com']
    # start_urls = ['http://www.smianet.com/Page.aspx?Id=7']
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
    def start_requests(self):
        try:
            header = {
                'Host':'www.smianet.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
            for x in range(1, 207):
                formData = {
                    '__VIEWSTATE': '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',
                    '__VIEWSTATEGENERATOR': '3989C74E',
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    'AspNetPager1_input': str(x),
                    'AspNetPager1': 'go'
                }
                yield scrapy.FormRequest('http://www.smianet.com/Page.aspx?Id=7',formdata=formData,headers=header,callback=self.parse_page,dont_filter=True)
        except Exception as e:
            logging.error(self.name + ": " + e.__str__())
            logging.exception(e)
    def parse_page(self, response):
        for url in response.css('#DatalistDetails a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_items, dont_filter=True)

    def parse_items(self, response):
        extractor = GeneralNewsExtractor()
        resp = response.text
        result = extractor.extract(resp, with_body_html=False)
        title = response.css('#lblTitle b::text').extract_first()
        txt = result['content']
        publish_time = result['publish_time']
        time = get_times(publish_time)
        item = HyxhItem()
        content_css = [
            '.BigFont'
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
        item['appendix'] = appendix
        item['source'] = '上海医疗器械行业协会'
        item['website'] =  '上海医疗器械行业协会'
        item['link'] = lyurl
        item['appendix_name'] = appendix_name
        item['type'] = 1
        item['tags'] = ''
        item['time'] = time
        item['content'] = content
        item['txt'] = txt
        item['spider_name'] = 'shanghai'
        item['module_name'] = '行业协会'
        yield item
