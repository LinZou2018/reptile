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


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Length": "5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "Hm_lvt_554c268f4979cd8ffd030cc4507df8c4=1534475117; JSESSIONID=740F887EE08A0DDF0A2C713EBD6F432E; Hm_lpvt_554c268f4979cd8ffd030cc4507df8c4=1534484238",
    "Host": "bishequ.com",
    "Origin": "http://bishequ.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://bishequ.com/exchangelist",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}



def UTCTime(timeout):
    # 判断时间是多久之前的
    pattern = re.compile("天")
    day = re.findall(pattern, timeout)
    pattern = re.compile("时")
    hour = re.findall(pattern, timeout)
    pattern = re.compile("分")
    minute = re.findall(pattern, timeout)
    pattern = re.compile("刚")
    nows = re.findall(pattern, timeout)
    pattern = re.compile("\d+")
    num = re.findall(pattern, timeout)[0]
    # 获取当前时间
    nowTheTime = int(time.time())
    # 计算新闻的发布的时间
    if len(day):
        marjin = int(num) * 24 * 60 * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(hour):
        marjin = int(num) * 60 * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(minute):
        marjin = int(num) * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(nows):
        return time.asctime(time.localtime(time.time()))
    else:
        # 如果是精确的时间就返回此时间
        return timeout