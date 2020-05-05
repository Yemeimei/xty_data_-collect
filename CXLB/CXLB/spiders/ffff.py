#encoding=utf-8
import re
from bs4 import BeautifulSoup
import datetime
import requests
import sys
import xlwt

reload(sys)
sys.setdefaultencoding("utf-8")
start = datetime.datetime.now()
count=0
book3 = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet_target3 = book3.add_sheet('test', cell_overwrite_ok=True)
try:
    for i in range(500):
        html_frist = "http://www.customs.gov.cn/eportal/ui?currentPage="+str(i)+"&moduleId=76777400f8cf4a66807d98d442234e97&pageId=374089"
        html = requests.get(html_frist)
        print html_frist
        html.encoding="utf-8"
        title = re.findall("target=\"_blank\" href=\"(.*)\" style",html.text)

        for each in title:
            #print each
            count+=1
            html_url = "http://www.customs.gov.cn"+each
            print "\t",html_url
            html1 = requests.get(html_url)
            html1.encoding = "utf-8"
            sensece = html1.text
            soup = BeautifulSoup(html1.text, 'html.parser')  # 文档对象

            str1=""
            for k in soup.findAll("div",class_="easysite-info-con"):
                str1 += str(k).replace("<div class=\"easysite-info-con\">","").replace("</div>","").replace("<p>","").replace("</p>","").replace("\n","").strip()+"@#$^@"
            #print str1[:-5]
            q = str1.split("@#$^@")[0]
            a = str1.split("@#$^@")[1]
            sheet_target3.write(count, 1, q)
            sheet_target3.write(count,2,a)
            book3.save("ceshi.xls")
            print count
            print "q",q
            print "w",a
except:
    print ("hh")
end =  datetime.datetime.now()
print ("耗时:%s S"%((end-start).seconds))