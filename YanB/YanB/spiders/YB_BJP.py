# -*- coding: utf-8 -*-
import logging

import scrapy
from gne import GeneralNewsExtractor

from YanB.items import YanbItem
from YanB.util_custom.tools.attachment import get_attachments, get_times
from YanB.util_custom.tools.cate import get_category


class YbBjpSpider(scrapy.Spider):
    name = 'YB_BJP'
    allowed_domains = ['swGridView.www']
    start_urls = ['http://www.cccmhpie.org.cn/ShowNewsList.aspx?QueryStr=x08x12o8q7x09x01w1z4892x9994y0998y6512x9982z0740z1350zO3w8w1u9v5v3v5zO3x10x02x11p4x2X12x01w1u8z8p2x01q9p4x2X12x01w1u9z8w7x08q7x15x15p3x0X14x18x0X14o3w8w1p3p9p3p3x0X14x18x0X14z8w7x08q7x15x15p4q7q8x08x01o8q7x09x01w1p3x2X15q5w7x08q7x15x15z8p5x10x05x13x17x01o3w8w1z8w8q7x16q7p3x0X14x18x0X14o3w8w1p3p9p3p3x0X14x18x0X14z8w8q7x16q7p4q7q8x08x01o8q7x09x01w1w8x11q9q5o0x05x14x15x16pQ7x03x01z8x00x0X15q9p5x10x05x13x17x01o3w8w1u9v5v3v5z8p2x1X1X16w7x08q7x15x15o3w8w1v7u8u9v5z8w7x08q7x15x15o3w8w1u9v5v3v5z8z2o6x05x10x07o3w8w1u9v5v3v5']
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
    def parse(self, response):
        for url in response.css('.swGridView a::attr(href)').extract():
            urls =response.urljoin(url)
            yield scrapy.Request(urls,callback=self.parse_item,dont_filter=True)

    def parse_item(self, response):
        item = YanbItem()
        resp = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(resp, with_body_html=False)
        title = result['title']
        txt = result['content']
        p_time = result['publish_time']
        content_css = [
            '.pagesContent'
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
        item['pub'] = '保健品'
        item['ctype'] = 3
        item['website'] = '保健品'
        item['txt'] = txt
        item['link'] = response.url
        item['spider_name'] = 'YB_BJP'
        item['module_name'] = '研报'
        item['tags'] = tags
        if content:
            yield item
