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
        for td in response.css('#DatalistDetails td'):
            yield scrapy.Request(response.urljoin(td.css('a::attr(href)').extract_first()), callback=self.parse_items, dont_filter=True,meta= {'time':td.css('font::text').extract_first()})
        # for url in response.css('#DatalistDetails a::attr(href)').extract():
        #     yield scrapy.Request(response.urljoin(url), callback=self.parse_items, dont_filter=True)

    def parse_items(self, response):
        extractor = GeneralNewsExtractor()
        resp = response.text
        result = extractor.extract(resp, with_body_html=False)
        title = response.css('#lblTitle b::text').extract_first()
        txt = result['content']
        time = get_times(response.meta['time'])
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
