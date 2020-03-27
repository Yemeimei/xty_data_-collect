import json
# import math
import time

import requests

def get_category(content):
    url = "http://39.96.199.128:9000/article/analysis"
    text = {
        'text': content
    }
    data = requests.post(url, data=text).text
    data = json.loads(data)
    status = data['status']
    classify = ''
    codes = ''
    if status == 'success':
        cates = data['category']
        areas = data['area']
        region = ''
        if areas:
            for area in areas:
                region = region + area + '|'
        for cate in cates:
            pro = cate['accuracy']
            pro = float(pro)
            if pro >= 0.05:
                cateName = cate['tagName']
                code = cate['tag']
                classify = classify + cateName + '|'
                codes = codes + code + '|'
    return classify, codes, region


if __name__ == '__main__':
    from lxml import etree
    url = 'http://www.zgyj.org.cn/indnews/071930205.html'
    html = requests.get(url).text
    soup = etree.HTML(html)
    content = soup.xpath("//div[@class='container']/div[@class='row']/div[@class='col-xs-12 col-sm-12 col-md-10 article_yq']/div[@class='nr']/div[3]//text()")
    print(content)
    content = ''.join(content).replace('\xa0', '').replace('\u3000', '').replace('\r', '').replace('\n',
                                                                                                   '').replace('\t',
                                                                                                               '').replace(
        ' ', '')
    s = time.time()
    cate, code, region = get_category(content)
    y = time.time()
    x = y - s
    print(cate, code, region)