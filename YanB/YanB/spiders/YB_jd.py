# -*- coding: utf-8 -*-
import json

import scrapy

from YanB.items import YanbItem
from YanB.util_custom.tools.attachment import get_attachments, get_times
from YanB.util_custom.tools.cate import get_category




class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
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
    start_urls = ['http://jd.com/']

    def start_requests(self):
        url = 'http://research.jd.com/industry/getIndustryList'
        for page in range(1, 7):
            param = {
                'page': str(page),
                'type': '0',
                'tc': '0'
            }
            yield scrapy.FormRequest(url, callback=self.parse, dont_filter=True, formdata=param)

    def parse(self, response):
        datas = json.loads(response.text)
        underlys = datas['data']['underly']
        for underly in underlys:
            appendix = underly['pdfUrl']
            title = underly['title']
            p_time = underly['cdate']
            id = underly['id']
            url = f'http://research.jd.com/content/contentDetail/toDetail?contentCode={id}'
            yield scrapy.Request(url, callback=self.parse_item,
                                 meta={'appendix': appendix, "title": title, 'p_time': p_time}, dont_filter=True)

    def parse_item(self, response):
        title = response.meta['title']
        appendix = response.meta['appendix']
        p_time = response.meta['p_time']
        content = response.css(".details-content ").extract()
        txt = response.css(".details-content ::text").extract()
        txt = ''.join(txt).replace('\t', '').replace('\r', '').replace('\n', '').replace('\xa0', '').replace(
            '\u3000', '').replace('\ue004', '').replace(' ', '')
        _, appendix_name = get_attachments(response)
        tags, _, _ = get_category(txt + title)
        industry = ''
        item = YanbItem()
        item['title'] = title
        item['p_time'] = get_times(str(p_time))
        item['industry'] = industry
        item['pub'] = '京东大数据研究院'
        item['ctype'] = 3
        item['website'] = '京东大数据研究院'
        item['link'] = response.url
        item['spider_name'] = 'jd'
        item['module_name'] = '研报'
        item['tags'] = tags
        item['appendix'] = appendix
        item['appendix_name'] = appendix_name
        item['content'] = ''.join(content)
        item['txt'] = txt
        if content:
            yield item
