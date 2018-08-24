import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, title_find


def storage(title, timeout, text):
    dicts = {
        "title": title,
        "release_time": timeout,
        "author": "比特币之家--快讯",
        "source": "比特币之家",
        "main": text,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="btc798_alerts")


# 发布时间，还未找到解决方案
# def UTCTime(timeout):
#     # 计算新闻的发布的时间
#     hour_one = timeout[:2]
#     date = time.localtime()
#     yaer = date.tm_year
#     mon = date.tm_mon
#     huor_two = date.tm_hour
#     if int(hour_one) > int(huor_two):
#         day = date.tm_mday - 1
#     else:
#         day = date.tm_mday
#     release_time = str(yaer) + "-" + str(mon) + "－" + day + " " + timeout



def download(object):
    texts = etree.tostring(object, method="text", encoding="utf8").decode("utf8").split()
    timeout = texts[0]
    data = texts[1:-3]
    text = ""
    for i in data:
        text += i + " "
    pattern = re.compile('(【[\s\S]*?】)([\s\S]*。)')
    title_text = re.findall(pattern, text)
    title = title_text[0][0]
    if title_find(title, come_from="btc798_alerts"):
        return True
    text = title_text[0][1]
    storage(title, timeout, text)


def getObject(html):
    print("btc798_alerts")
    # 快讯信息没有详情页
    html = etree.HTML(html)
    textObject = html.xpath('//*[@id="page-livenews"]/div[1]/div/div[2]/div/div')
    for i in textObject:
        data = download(i)
        if data:
            break


def starts():
    url = "http://www.btc798.com/live.html"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        getObject(html)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()