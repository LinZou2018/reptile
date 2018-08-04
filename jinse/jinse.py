import requests
from lxml import etree
import threading
import re

from error_document import mistake
from headers import header
from mongodb_news import *

def storage(title, author, times, page_view, source, mains,number):
    # 存入数据库
    time = ""
    main = ""
    for i in times:
        time += i
    for i in mains:
        main += i
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "time": time,
        "page_view": page_view,
        "source": source,
        "main": main,
    }
    storageDatabase(dicts, come_from="jinse")


def download(url, reponse):
    try:
        # 筛选数据
        html = etree.HTML(reponse.text)
        texts = html.xpath('//div[@class="js-article"]')[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        title = text[0]
        author = text[1]
        times = text[2: 4]
        page_view = text[4]
        source = "金色财经" + ":" + url
        mains = text[5:]
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)
        # 进行存储
        storage(title, author, times, page_view, source, mains, number)
    except Exception as err:
        mistake(url, err)

def titleUrl(url, headers):
    reponse = requests.get(url, headers = headers)
    reponse.encoding = "utf-8"
    # 查询在数据库中是否已经存在
    pattern_num = re.compile('\d+')
    number = re.findall(pattern_num, url)[0]
    # 判断数据库中是否已经下载过
    if rechecking(number, come_from="jinse"):
        return
    # 判断是否加载完成
    if reponse.status_code == 200:
        # 匹配下一篇新闻的url
        html = reponse.text
        pattern = re.compile('<ol>下一篇</ol>[\s\S]*?</h2>')
        texts = re.findall(pattern, html)[0]
        # print(texts)
        pattern = re.compile('https://[\s\S]*?\d+.html')
        url = re.findall(pattern, texts)[0]
        # print(href)
    else:
        err = "reponse.status_code为:" + reponse.status_code
        mistake(url, err)
        return reponse.status_code
    # 创建线程爬去数据
    return reponse.status_code


def starts(headers):
    # 从首页开始查询网址
    url = "https://www.jinse.com"
    reponse = requests.get(url, headers = headers)
    reponse.encoding = "utf-8"
    html = reponse.text
    # 获取首页所有的新闻网址
    pattern = re.compile('[a-zA-z]+://www.jinse.com[^\s]*\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    n = 1
    for url in urls:
        value = reponse.status_code
        # 循环获取下一篇内容
        while True:
            if value == "exist":
                print("数据已经存在")
                break
            elif value == 200:
                value = titleUrl(url, headers)
            else:
                print("结束")
                break
            n += 1


if __name__ == "__main__":
    starts(header())


