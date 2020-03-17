# -*- coding: utf-8 -*-
import logging

import scrapy
from gne import GeneralNewsExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from HY_NEWS.items import HyNewsItem
from HY_NEWS.util_custom.tools.attachment import get_times
from HY_NEWS.util_custom.tools.cate import get_category



script = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return {
    html = splash:html(),
    har = splash:har(),
  }
end
"""
class SohuAutoSpider(CrawlSpider):
    name = 'sohu_auto'
    allowed_domains = ['auto.sohu.com']
    start_urls = ['http://auto.sohu.com/qichexinwen.shtml']
    custom_settings = {
        # 并发请求
        'CONCURRENT_REQUESTS': 10,
        # 'CONCURRENT_REQUESTS_PER_DOMAIN': ,
        'CONCURRENT_REQUESTS_PER_IP': 0,
        # 下载暂停
        'DOWNLOAD_DELAY': 0.5,
        'ITEM_PIPELINES': {
            # 设置异步入库方式
            'HY_NEWS.pipelines.MysqlTwistedPipeline': 600,
            # 去重逻辑
            # 'HY_NEWS.pipelines.DuplicatesPipeline': 200,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 调用 scrapy_splash 打开此设置
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,

            # 设置设置默认代理
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 700,
            # 设置请求代理服务器
            # 'HY_NEWS.util_custom.middleware.middlewares.ProxyMiddleWare': 100,
            # 设置scrapy 自带请求头
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            # 自定义随机请求头
            'HY_NEWS.util_custom.middleware.middlewares.MyUserAgentMiddleware': 120,
            # 重试中间件
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            # 重试中间件
            'HY_NEWS.util_custom.middleware.middlewares.MyRetryMiddleware': 90,
        },
        # 调用 scrapy_splash 打开此设置
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        # 去重/api端口
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        # # 'SPLASH_URL': "http://10.8.32.122:8050/"
        'SPLASH_URL': "http://127.0.0.1:8050/"
    }

    def start_requests(self):
        url ='http://auto.sohu.com/qichexinwen.shtml'
        yield SplashRequest(url, args={'lua_source': script, 'wait': 1}, callback=self.parse,dont_filter=True)

    def parse(self, response):
        resp =response
        print(type(resp))

    def parse_item(self, response):
        item = HyNewsItem()
        resp = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(resp, with_body_html=False)
        title = result['title']
        txt = result['content']
        p_time = result['publish_time']
        content_css = [
            '.TRS_Editor',
            '.detail_content',
            '.block_left',
            '.detail_content',
            '.content-text',
        ]
        lyurl = response.url
        lyname = '中国工业新闻网'
        for content in content_css:
            content = ''.join(response.css(content).extract())
            if content:
                break
            if not content:
                logging.warning(f'{response.url}' + '当前url无 css 适配未提取 centent')
        classify, codes, region = get_category(txt)
        item['title'] = title
        item['txt'] = txt
        item['p_time'] = get_times(p_time)
        item['content'] = content
        item['spider_name'] = 'sohu_auto'
        item['module_name'] = '行业新闻'
        item['cate'] = classify
        item['region'] = region
        item['code'] = codes
        item['link'] = lyurl
        item['website'] = lyname
        if content:
            yield item