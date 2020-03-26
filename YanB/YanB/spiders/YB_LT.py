# -*- coding: utf-8 -*-
import logging
import re
import time

import scrapy
from gne import GeneralNewsExtractor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from YanB.items import YanbItem
from YanB.util_custom.tools.attachment import get_times, get_attachments
from YanB.util_custom.tools.cate import get_category


class YbLtSpider(scrapy.Spider):
    name = 'YB_LT'
    allowed_domains = ['www.bianews.com']
    # start_urls = ['https://www.bianews.com/news/yanbao/']
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
    def start_requests(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("debuggerAddress", '127.0.0.1:99992')
        url = 'https://www.bianews.com/news/yanbao'
        driver = webdriver.Chrome('/Users/yemiemie/xty_data/YanB/YanB/util_custom/chromedriver',
                                  chrome_options=chrome_options)
        driver.get(url)
        time.sleep(1)
        respo = driver.page_source
        urls = re.findall('id="(\d+)"', ''.join(respo))
        driver.quit()
        for url in urls:
            if len(url) == 5:
                url ='https://www.bianews.com/news/details?id='+url
                yield scrapy.Request(url,callback=self.parse,dont_filter=True)


    def parse(self, response):
        item = YanbItem()
        resp = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(resp, with_body_html=False)
        title = result['title']
        txt = result['content']
        p_time = result['publish_time']
        content_css = [
            '.body'
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
        item['pub'] = '链塔'
        item['ctype'] = 3
        item['website'] = '链塔'
        item['txt'] = ''.join(txt).strip()
        item['link'] = response.url
        item['spider_name'] = 'YB_LT'
        item['module_name'] = '研报'
        item['tags'] = tags
        if content:
            yield item
