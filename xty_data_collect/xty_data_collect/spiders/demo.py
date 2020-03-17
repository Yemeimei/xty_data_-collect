# -*- coding: utf-8 -*-
import scrapy

from gne import GeneralNewsExtractor

from xty_data_collect.items import XtyDataCollectItem
from xty_data_collect.util_custom.tools.attachment import get_content_css, get_attachments, get_times
import logging
class DemoSpider(scrapy.Spider):
    name = 'demo'#爬虫名称
    # allowed_domains = ['']#限制提取域名  注释掉
    start_urls = ['http://neimenggu.chinatax.gov.cn/zxfb/index_1.html']# 开始 url
    custom_settings = {
        #并发请求
        'CONCURRENT_REQUESTS': 10,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        #下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            #设置异步入库方式
            'xty_data_collect.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'investment_news.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            # 'scrapy_splash.SplashCookiesMiddleware': 723,
            # 'scrapy_splash.SplashMiddleware': 725,


            #设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            #设置请求代理服务器
            # 'xty_data_collect.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            #设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            #自定义随机请求头
            'xty_data_collect.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            #重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            #重试中间件
            'xty_data_collect.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
        },
        # 调用 scrapy_splash 打开此设置
        # 'SPIDER_MIDDLEWARES': {
        #     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        # },
        #去重/api端口
        # 'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # # 'SPLASH_URL': "http://10.8.32.122:8050/"
        # 'SPLASH_URL': "http://127.0.0.1:8050/"
    }

    # def start_requests(self):
    # '''
    # 此函数存在时 start_urls 无效
    # url : http连接 完整
    # callback: 回调传参 ,
    # dont_filter: scrapy 去重中间件建议打开避免报错
    # '''
    #

    def parse(self,response):
        '''
        url : http连接 完整
        callback: 回调传参 ,
        dont_filter: #scrapy 去重中间件建议打开避免报错
        '''
        for url in response.css('.snewslist a::attr(href)').extract():
            url =response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        '''
        实际解析页面根据页面实际情况进行解析
        '''
        item =XtyDataCollectItem()
        resp=response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(resp,with_body_html=False)
        title =result['title']
        txt =result['title']
        p_tiem =result['publish_time']
        for conte in get_content_css():
            try:
                content = response.css(conte).extact()
                if content:
                    content = content
                    break
            except:
                logging.warning('正文获取失败,请检查')
        appendix, appendix_name = get_attachments(response)
        item['title'] =title
        item['txt'] =txt
        item['p_tiem'] = get_times(p_tiem)
        item['content'] = content
        item['appendix']=appendix
        item['appendix_name']=appendix_name
        yield item

