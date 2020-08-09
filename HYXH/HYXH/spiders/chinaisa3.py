# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from gne import GeneralNewsExtractor
from scrapy.selector import Selector
import logging
import json
from scrapy.spiders import CrawlSpider, Rule

from HYXH.items import HyxhItem
from HYXH.util_custom.tools.attachment import get_attachments, get_times


class HySpider(CrawlSpider):
    name = 'chinaisa3'
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
                'Content-Type':' application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
            for x in range(1, 46):
                formData = {
                    'params': '%7B%22columnId%22:%221b4316d9238e09c735365896c8e4f677a3234e8363e5622ae6e79a5900a76f56%22,%22param%22:%22%257B%2522pageNo%2522:'+str(x)+',%2522pageSize%2522:25%257D%22%7D'
                }
                yield scrapy.FormRequest('http://www.chinaisa.org.cn/gxportal/xfpt/portal/getColumnList',formdata=formData,headers=header,callback=self.parse_page,dont_filter=True)
        except Exception as e:
            logging.error(self.name + ": " + e.__str__())
            logging.exception(e)
    def parse_page(self, response):
        header = {
            'Content-Type': ' application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        data = json.loads(response.text)
        selector = Selector(text=data['articleListHtml'])
        for url in selector.css('.list a::attr(href)').extract():
            articleId = url.split('=')[1]
            articleId = articleId.split('&')[0]
            formData = {
                'params': '%7b%22articleId%22%3a%22'+str(articleId)+'%22%2c%22columnId%22%3a%221b4316d9238e09c735365896c8e4f677a3234e8363e5622ae6e79a5900a76f56%22%7d'
            }
            yield scrapy.FormRequest('http://www.chinaisa.org.cn/gxportal/xfpt/portal/viewArticleById', formdata=formData,
                                     headers=header, callback=self.parse_items, dont_filter=True,meta={'url':'http://www.chinaisa.org.cn/gxportal/xfgl/portal/' + str(url)})
    def parse_items(self, response):
        data = json.loads(response.text)
        selector = Selector(text=data['article_content'])
        title = ''.join(selector.css('.article_title::text').extract())
        time = get_times(selector.css('.article_title p::text').extract_first())
        item = HyxhItem()
        content = ''.join(selector.css('.article_main').extract())
        txt = ''.join(selector.css('.article_main *::text').extract())
        item['title'] = title
        appendix, appendix_name = get_attachments(selector)
        item['appendix'] = appendix
        item['source'] = '中国钢铁工业协会-行业分析报告'
        item['website'] =  '中国钢铁工业协会'
        item['link'] = response.meta['url']
        item['appendix_name'] = appendix_name
        item['type'] = 3
        item['tags'] = ''
        item['time'] = time
        item['content'] = content
        item['txt'] = txt
        item['spider_name'] = 'chinaisa3'
        item['module_name'] = '行业协会'
        yield item
