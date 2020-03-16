import scrapy
import logging
import re

def get_attachments(response):
    valid_extensions = [".doc", ".docx", ".xlsx", ".xls", ".pdf", ".zip", ".wps", ".rar"]
    # 取所有超链接
    list = response.xpath("//a")
    appendix=""
    appendix_name=""
    for a in list:
        # 取超链接文本
        href = a.xpath('./@href').extract_first()
        name = a.xpath('./text()').extract_first()
        if href and name:
            for ext in valid_extensions:
                if href.endswith(ext) or name.endswith(ext):
                    appendix = appendix + response.urljoin(href) + ","
                    appendix_name = appendix_name + name + ","
    return appendix, appendix_name

#时间格式化
def get_times(srcTime):
    result = srcTime
    if isinstance(srcTime, str):
        list = re.findall(r'([1-9]\d*?\d*)', srcTime)
        if len(list) == 1 and len(list[0]) == 8:  # eg:20190810
            result = list[0][:4] + '-' + list[0][4:6] + '-' + list[0][6:]
        elif len(list) > 2:
            result = list[0] + '-' + list[1].zfill(2) + '-' + list[2].zfill(2)
        else:
            if srcTime != '':
                logging.error('时间格式化异常：' + srcTime)
    return result
#根据来源进行分类
def get_shijian(scrEvent):
    result = scrEvent
    merge =('并购')
    listed =('Pre-IPO','IPO上市及以后','定向增发','新三板','新三板定增','退市')
    invest =('未融资','种子轮','不详','种子','天使轮','天使','Pre-A','A轮','A+轮','Pre-B','B轮','B+轮','Pre-C','C轮','C+轮','Pre-D','D轮','D+轮','Pre-E','E轮','E+轮','Pre-F','F轮','F+轮','股权转让','战略投资','不明确','尚未获投','股权投资','其他轮')
    cname =''
    if result.endswith(merge):
        cname = cname+'bgsj'
    elif result.endswith(listed):
        cname =cname +'sssj'
    elif result.endswith(invest):
        cname = cname+'tzsj'
    return result,cname

def dispose_moncht(scrmonth):
    result =str(scrmonth)
    if len(result) ==  1:
        month = '0'+result
    else:
        month = result
    return month