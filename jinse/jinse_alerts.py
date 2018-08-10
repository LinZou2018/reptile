import requests
from lxml import etree
import re
import json
import time
from error_document import mistake
import headers
from mongodb_news import *


def storage(titles, authors, times, url, mains):
    # 存入
    title = ""
    author = ""
    time = ""
    main = ""
    for i in titles:
        title += i
    authors[0] = "金色财经"
    for i in authors:
        author += i
    for i in times:
        time += i
    for i in mains:
        main += i
    dicts = {
        "title": title,
        "author": author,
        "time": time,
        "URL": url,
        "main": main,
    }
    storageDatabase(dicts, come_from="jinse_alerts")


def download(url):
    print("jinse_alerts")
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    # 判断网页是否加载完成
    if reponse.status_code == 200:
        # 匹配时间正文再加以组合
        try:
            html = etree.HTML(reponse.text)
            texts = html.xpath('//*[@class="tc"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            times = text[0] + text[1]
            texts = html.xpath('//*[@class="time-detail"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            times = times + "--" + text[0]
            texts = html.xpath('//*[@class="intro-detail"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            titles = text[0: 3]
            authors = text[-5:]
            mains = text[3: -5]
            storage(titles, authors, times, url, mains)
        except Exception as err:
            mistake(url, err)
        return False
    else:
        err = reponse.status_code
        mistake(url, err)
        return True


def getUrl():
    number = max_id(come_from="jinse_alerts")
    if number:
        num = number
    else:
        num = 44400
        while True:
            # 判断数据库中是否已经下载过
            if rechecking(number=num, come_from="jinse_alerts"):
                break
            url = "https://www.jinse.com/lives/%s.htm" % num
            end = download(url)
            if end:
                break
            num -= 1
        num = 44400

    while True:
        num += 1
        # 判断数据库中是否已经下载过
        if rechecking(number=num, come_from="jinse"):
            return
        url = "https://www.jinse.com/lives/%s.htm" % num
        end = download(url)
        if end:
            break


def starts():
    s = 0
    while True:
        try:
            url = "https://www.jinse.com/lives"
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                getUrl()
                break
            else:
                err = reponse.status_code
                mistake(url, err)
                # 网页可以重新加载三次
                if s == 2:
                    break
                s += 1
        except:
            if s == 2:
                break
            s += 1


# def storage(findOne, release_time):
#     dicts = findOne
#     dicts["createText"] = release_time
#     storageDatabase(dicts, come_from="btc123_alerts")
#
# def download(reponse, url):
#     try:
#         print("btc123_alerts")
#         html = reponse.text
#         # 将文档的json转换为字典
#         texts = json.loads(html)
#         data = texts["list"]
#         # 获取更精确的时间
#         release_time = data["date"]
#         text = data["lives"]
#         for findOne in text:
#             number = findOne["id"]
#             if rechecking(number, "btc123_alerts"):
#                 break
#             storage(findOne, release_time)
#     except Exception as err:
#         # mistake(url, err)
#         pass
#
#
# def starts():
#     n = 44502
#     s = 0
#     while True:
#         url = "https://api.jinse.com/v4/live/list?limit=20&reading=false&flag=up&id=%s" % n
#         try:
#             reponse = requests.get(url, headers=headers.header())
#             reponse.encoding = "utf-8"
#             # 判断网页是否加载完成
#             if reponse.status_code == 200:
#                 download(reponse, url)
#                 n -= 20
#             else:
#                 err = reponse.status_code
#                 # mistake(url, err)
#                 # 网页有三次重新加载
#                 if s == 2:
#                     break
#                 s += 1
#         except:
#             # 网页可以重新加载
#             if s == 2:
#                 break
#             s += 1
#         break


if __name__ == "__main__":
    starts()
