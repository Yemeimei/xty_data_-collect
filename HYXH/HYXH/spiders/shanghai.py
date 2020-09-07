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
        yield scrapy.Request('http://www.smianet.com/Page.aspx?Id=7', callback=self.parse_page1)

    def parse_page1(self, response):
        value = response.css('#__VIEWSTATE::attr(value)').extract_first()
        try:
            header = {
                'Host':'www.smianet.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
            for x in range(1, 209):
                print('x' + str(x))
                formData = {
                    '__VIEWSTATE': value,
                    '__VIEWSTATEGENERATOR': '3989C74E',
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    'AspNetPager1_input': str(x),
                    'AspNetPager1': 'go'
                }
                yield scrapy.FormRequest('http://www.smianet.com/Page.aspx?Id=7', formdata=formData, headers=header, callback=self.parse_page, dont_filter=True)
        except Exception as e:
            logging.error(self.name + ": " + e.__str__())
            logging.exception(e)
    def parse_page(self, response):
        for td in response.css('#DatalistDetails td'):
            yield scrapy.Request(response.urljoin(td.css('a::attr(href)').extract_first()), callback=self.parse_items, dont_filter=True, meta={'time': td.css('font::text').extract_first()})


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
        if content:
            item['title'] = title
            appendix, appendix_name = get_attachments(response)
            item['appendix'] = appendix
            item['source'] = '上海医疗器械行业协会'
            item['website'] = '上海医疗器械行业协会'
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
