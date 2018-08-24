import json
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(article, timeout, text, img):
    dicts = {
        "_id": article["articleId"],
        "title": article["articleTitle"],
        "author": article["articleEditor"],
        "release_time": timeout,
        "source": "币社区新闻",
        "main": text,
        "label": article["articleKeyword"],
        "img": img,
        "statement": "声明：本文观点仅代表作者本人，绝不代表币社区赞同其观点或证实其描述。版权属币社区所有，未经授权不得转载。",
    }
    # print(dicts)
    storageDatabase(dicts, come_from="bishequ")


def download(article):
    print("bishequ")
    timeout = time.asctime(time.localtime(int(article["articleCreateTime"])/1000))
    texts = article["articleContent"]
    html = etree.HTML(texts)
    text = etree.tostring(html, method="text", encoding="utf8").decode("utf8")
    img = html.xpath('//img/@src')
    storage(article, timeout, text, img)


def connent(reponse):
    html = reponse.text
    data = json.loads(html)
    articleList = data["articleList"]
    for article in articleList:
        number = article["articleId"]
        if rechecking(number, come_from="bishequ"):
            break
        download(article)


def starts():
    url = "http://bishequ.com/article/getArticleList"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        connent(reponse)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()