import requests
from lxml import etree
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


def download(url, reponse, number):
    try:
        print("jinse")
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
        # 进行存储
        storage(title, author, times, page_view, source, mains, number)
    except Exception as err:
        mistake(url, err)

def titleUrl(url, headers):
    s = 0
    while True:
        try:
            reponse = requests.get(url, headers = headers)
            reponse.encoding = "utf-8"
            # 查询在数据库中是否已经存在
            pattern_num = re.compile('\d+')
            number = re.findall(pattern_num, url)[0]
            # 判断数据库中是否已经下载过
            if rechecking(number, come_from="jinse"):
                break
            # 判断是否加载完成
            if reponse.status_code == 200:
                download(url, reponse, number)
                # 匹配下一篇新闻的url
                html = reponse.text
                pattern = re.compile('<ol>下一篇</ol>[\s\S]*?</h2>')
                texts = re.findall(pattern, html)[0]
                # print(texts)
                pattern = re.compile('https://[\s\S]*?\d+.html')
                url = re.findall(pattern, texts)[0]
                # print(href)
            else:
                err = reponse.status_code
                mistake(url, err)
                if s == 3:
                    break
                s += 3
        except:
            if s == 3:
                break
            s += 1


def starts(headers):
    # 从首页开始查询网址
    s = 0
    url = "https://www.jinse.com"
    while True:
        reponse = requests.get(url, headers = headers)
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            # 获取首页所有的新闻网址
            pattern = re.compile('[a-zA-z]+://www.jinse.com[^\s]*\.html')
            urls = re.findall(pattern, html)
            urls = list(set(urls))
            for url in urls:
                if reponse.status_code == 200:
                    titleUrl(url, headers)
                else:
                    err = reponse.status_code
                    mistake(url, err)
                    break
            break
        else:
            # 有三次重新加载网页
            if s == 3:
                err = reponse.status_code
                mistake(url, err)
                break
            s += 1


if __name__ == "__main__":
    starts(header())


