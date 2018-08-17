import requests
from lxml import etree
# import json
import threading
import re

listHeaders = [
    {"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
    {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
    {"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"},
    {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
    {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
    {"User-Agent":"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11"},
    {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"},
    {"User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"},
    ]
#
# for headers in listHeaders:
#     url = 'http://www.fn.com/lives'
#     reponse = requests.get(url, headers)
#     reponse.encoding = "utf-8"
#     html = etree.HTML(reponse.text)
#     down = html.xpath('//*[@id="wrap"]/div/div/div/div[2]/div[5]/div[1]/h2/a/@href')
#     print(down)

str = '''<div class="new_info_title">
                            <p class="new_info_h1">南非当局拟对加密货币征税，民间社群表示欢迎——征税体现当局对加密货币的接纳</p>
                            <p class="new_info_p cl"><i class="icon icon-time"></i>2018-08-09 17:59:24<span>
                                     
                                        来源：币报道                                </span></p>

                        </div>'''

p = re.compile('(>)([\s\S]*?)(<)')
m = re.findall(p, str)
print(m)