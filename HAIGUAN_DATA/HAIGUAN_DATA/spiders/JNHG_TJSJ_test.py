# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from HAIGUAN_DATA.items import HaiguanDataItem
from HAIGUAN_DATA.util_custom.tools.attachment import get_attachments, get_times
from selenium import webdriver

class JnhgTjsjSpider(scrapy.Spider):
    name = 'JNHG_TJSJ_test'
    # start_urls = ['http://39.96.199.128:8888/getCookie?url=http://beijing.customs.gov.cn/eportal/ui?pageId=434774&currentPage=1&moduleId=1667380986bc42c583c65be8d74da7d1&staticRequest=yes']

    def __init__(self, cookie={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cookie = cookie
    # allowed_domains = ['http://beijing.customs.gov.cn/jinan_customs/500341/500343/500344/index.html']
    # start_urls = ['http://changchun.customs.gov.cn/changchun_customs/465846/465848/49e6d0b3-1.html']

    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        # 下载暂停
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'HAIGUAN_DATA.pipelines.MysqlTwistedPipeline': 600,
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
            'HAIGUAN_DATA.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            'HAIGUAN_DATA.util_custom.middleware.middlewares.WangyiproDownloaderMiddleware': 180,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'HAIGUAN_DATA.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
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

    # 重写start_requests方法
    def start_requests(self):
        urls = 'http://39.96.199.128:8888/getCookie?url=http://beijing.customs.gov.cn/eportal/ui?pageId=434774&currentPage=1&moduleId=1667380986bc42c583c65be8d74da7d1&staticRequest=yes'
        yield scrapy.Request(urls, callback=self.parseCookie, meta={
            'url': 'http://beijing.customs.gov.cn/eportal/ui?pageId=434774&currentPage=1&moduleId=1667380986bc42c583c65be8d74da7d1&staticRequest=yes'},
                             dont_filter=True, priority=10)

    def parseCookie(self, response):
        print(response.text)
        if len(str(response.text)) > 10:
            self.cookie = json.loads(response.text)
        yield scrapy.Request(response.meta['url'],  callback=self.parse, dont_filter=True)

    def parse(self, response):
        if response.status == 209:
            urls = 'http://39.96.199.128:8888/getCookie?url=' + str(response.url)
            yield scrapy.Request(urls, callback=self.parseCookie, meta={'url': str(response.url)}, dont_filter=True, priority=10)
        else:
            page_id = response.css(
                '#eprotalCurrentPageId::attr(value)').extract_first()
            module_id = response.css(
                'input[name=article_paging_list_hidden]::attr(moduleid)').extract_first()
            url = 'http://beijing.customs.gov.cn/eportal/ui?pageId=' + page_id + \
                  '&currentPage=1&moduleId=' + module_id + '&staticRequest=yes'
            yield scrapy.Request(url,  callback=self.parse_total, meta=response.meta, dont_filter=True)

    def parse_total(self, response):
        if response.status == 209:
            urls = 'http://39.96.199.128:8888/getCookie?url=' + str(response.url)
            yield scrapy.Request(urls, callback=self.parseCookie, meta={'url': str(response.url)}, dont_filter=True,
                                 priority=10)
        else:
            page_count = int(response.css(
                'input[name=article_paging_list_hidden]::attr(totalpage)').extract_first())
            page_id = response.css(
                '#eprotalCurrentPageId::attr(value)').extract_first()
            module_id = response.css(
                'input[name=article_paging_list_hidden]::attr(moduleid)').extract_first()
            for page_num in range(page_count):
                url = 'http://beijing.customs.gov.cn/eportal/ui?pageId=' + page_id + '&currentPage=' + \
                      str(page_num + 1) + '&moduleId=' + module_id + '&staticRequest=yes'
                yield scrapy.Request(url,  callback=self.parse_list, meta=response.meta, dont_filter=True)

    def parse_list(self, response):
        if response.status == 209:
            urls = 'http://39.96.199.128:8888/getCookie?url=' + str(response.url)
            yield scrapy.Request(urls, callback=self.parseCookie, meta={'url': str(response.url)}, dont_filter=True,
                                 priority=10)
        else:
            for href in response.css('.conList_ul a::attr(href)').extract():
                url = response.urljoin(href).strip()
                if (url.endswith('.html') or url.endswith('.htm')) and url.startswith(
                        'http://') and (url != response.url):
                    yield scrapy.Request(url,  callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        if response.status == 209:
            urls = 'http://39.96.199.128:8888/getCookie?url=' + str(response.url)
            yield scrapy.Request(urls, callback=self.parseCookie, meta={'url': str(response.url)}, dont_filter=True,
                                 priority=10)
        else:
            try:
                item = HaiguanDataItem()
                item['title'] = response.css('title::text').extract_first()
                item['time'] = get_times(
                    response.css('.easysite-news-describe::text').extract_first())
                item['content'] = response.css('#easysiteText').extract_first()
                appendix, appendix_name = get_attachments(response)
                item['appendix'] = appendix
                item['appendix_name'] = appendix_name
                item['name'] = '中华人民共和国济南海关'
                item['website'] = '中华人民共和国济南海关-统计数据'
                item['link'] = response.url
                item['txt'] = ''.join(
                    response.css('#easysiteText *::text').extract())
                item['module_name'] = '中华人民共和国济南海关-统计数据'
                item['spider_name'] = 'JNHG_TJSJ'
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