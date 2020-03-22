# -*- coding: utf-8 -*-
import logging

import scrapy
from gne import GeneralNewsExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from YanB.items import YanbItem
from YanB.util_custom.tools.attachment import get_attachments, get_times
from YanB.util_custom.tools.cate import get_category


class YbYmSpider(CrawlSpider):
    name = 'YB_YM'
    allowed_domains = ['youcloud.com']
    start_urls = ['https://youcloud.com/reports']

    rules = (
        Rule(LinkExtractor(restrict_css='.article-list a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = YanbItem()
        resp = response.text
        extractor = GeneralNewsExtractor()
        result = extractor.extract(resp, with_body_html=False)
        title = result['title']
        txt = result['content']
        p_time = result['publish_time']
        content_css = [
            '.content'
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
        item['pub'] = '有米'
        item['ctype'] = 3
        item['website'] = '有米'
        item['txt'] = txt
        item['link'] = response.url
        item['spider_name'] = 'YB_YM'
        item['module_name'] = '研报'
        item['tags'] = tags
        if content:
            yield item
