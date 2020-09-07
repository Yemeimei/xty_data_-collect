# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from gne import GeneralNewsExtractor
import re
import logging
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from HYXH.items import HyxhItem
from HYXH.util_custom.tools.attachment import get_attachments, get_times


class HySpider(CrawlSpider):
    name = 'zhejiang_clxh1'
    allowed_domains = ['www.xclcy.com']
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
        for x in range(1, 10):
            yield scrapy.Request('http://www.xclcy.com/info/list.php?catid=2374&page=' + str(x), callback=self.parse)

    def parse(self, response):
        start = response.text.index('<div class="body">')
        end = response.text.index('<script type=”text/javascript”>show_task')
        text = response.text[start:end]
        selector = Selector(text=text)
        for url in selector.css('.ind_all_news4 a::attr(href)').extract():
            yield scrapy.Request(url, callback=self.parse_items, dont_filter=True)
        # for url in urls:
        #     print(url)
        #     yield scrapy.Request(url, callback=self.parse_items, dont_filter=True)

    def parse_items(self, response):
        start = response.text.index('<div class="wrapper">')
        text = response.text[start:]
        selector = Selector(text=text)
        lyurl = response.url
        title = selector.css('.titles h1::text').extract_first()
        publish_times = selector.css('.titles .fl::text').extract()
        publish_time = publish_times[1]
        time = get_times(publish_time)
        item = HyxhItem()
        content_css = [
            '.inf_arct'
        ]
        for content in content_css:
            content = ''.join(selector.css(content).extract())
            if content:
                break
            if not content:
                logging.warning(f'{response.url}' + '当前url无 css 适配未提取 centent')
        if content:
            txt = ''.join(selector.xpath('//div[@id="article"]//text()').extract())
            item['title'] = title
            appendix, appendix_name = get_attachments(selector)
            item['appendix'] = appendix
            item['source'] = '浙江省新材料产业协会'
            item['website'] = '浙江省新材料产业协会'
            item['link'] = lyurl
            item['appendix_name'] = appendix_name
            item['type'] = 1
            item['tags'] = ''
            item['time'] = time
            item['content'] = content
            item['txt'] = txt
            item['spider_name'] = 'zhejiang_clxh1'
            item['module_name'] = '行业协会'
            yield item

