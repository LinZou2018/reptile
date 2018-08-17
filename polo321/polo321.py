import requests
from lxml import etree
import json
import headers
import time
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(data, timeout, main_text, img):
    dicts = {
        "_id": data["id"],
        "title": data["title"],
        "author": data["author"],
        "release_time": timeout,
        "source": data["source"],
        "main": main_text,
        "label": data["tags"],
        "img": img,
    }
    storageDatabase(dicts, come_from="polo321")


def download(number):
    # 连接新闻具体信息
    url = 'http://39.108.117.97:8082/geek/infoDetail/1/%s' % number
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        # 获取信息的内容
        html = reponse.text
        # 将json格式文本转换为字典
        texts = json.loads(html)
        data = texts["data"]
        # 转换时间，获取发布时间
        num = float(data["releasedTime"]) / 1000
        timeout = time.asctime(time.localtime(num))
        # 在html文本中获取新闻内容
        main_html = data["content"]
        main_html = etree.HTML(main_html)
        main_text = etree.tostring(main_html, method="text", encoding="utf8").decode("utf8").split()
        # 获取所使用的图片
        img = main_html.xpath('//img/@src')
        storage(data, timeout, main_text, img)
    else:
        err = reponse.status_code
        mistake(url, err)

def getUrl(reponse):
    print("polo321")
    # 获取排列新闻的信息
    html = reponse.text
    texts = json.loads(html)
    data = texts["data"]
    # 获取其中信息
    texts = data["list"]
    # 判断是否获取到信息，如果没有则说明已经超出翻页范围，则结束翻页获取信息，
    if not texts:
        return True
    for text in texts:
        # 分离出编号，以编号去获取具体新闻内容
        number = text["id"]
        if rechecking(number, come_from="polo321"):
            return True
        download(number)


def starts():
    # 网站新闻信息网址
    urls = ['http://39.108.117.97:8082/hotNewsList?size=10&page=%s&subType=',
            "http://39.108.117.97:8082/blockChainList?size=10&page=%s&subType="]
    for i in urls:
        subType = 0
        # 新闻信息的分类，都分为3类共6类新闻
        while subType < 3:
            page = 1
            url_page = i + str(subType)
            # 新闻信息翻页获取url
            while True:
                url = url_page % page
                reponse = requests.get(url, headers=headers.header())
                reponse.encoding = "utf-8"
                if reponse.status_code == 200:
                    data = getUrl(reponse)
                    if data:
                        break
                else:
                    err = reponse.status_code
                    mistake(url, err)
                    break
                page += 1
            subType += 1


if __name__ == '__main__':
    starts()