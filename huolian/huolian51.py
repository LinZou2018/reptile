import json
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "deviceType": "H5",
    "Host": "api.huolian.online",
    "nitToken": "",
    "Origin": "https://huolian.com",
    "Referer": "https://huolian.com/fire.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
}


def storage(data, text, img):
    dicts = {
        "_id": data["fcNewsAuthorId"],
        "title": data["fcNewsTitle"],
        "author": data["fcNewsAuthorName"],
        "release_time": data["fcNewsDate"],
        "content_source": data["fcNewsSource"],
        "main": text,
        "source": "火链财经",
        "img": img,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="huolian")


def download(html):
    print("huolian")
    html = json.loads(html)
    data = html["data"]
    number = data["fcNewsAuthorId"]
    if rechecking(number, come_from="huolian"):
        return
    mse = data["fcNewsContent"]
    texts = etree.HTML(mse)
    text = texts.xpath("//p/text()")
    img = texts.xpath("//img/@src")
    storage(data, text, img)


def connent(number):
    data = {
        "newsId": number,
    }
    url = "https://api.huolian.online/nit/news/newsParticulars"
    reponse = requests.post(url, data=data, headers=headers)
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        download(html)
    else:
        err = reponse.status_code
        mistake(url, err)
        return True


def findNumber(html):
    html = json.loads(html)
    data = html["data"]
    reload = 0
    for text in data:
        number = text["fcNewsId"]
        if rechecking(number, come_from="huolian"):
            if reload == 3:
                return True
            else:
                reload += 1
                continue
        data = connent(number)
        if data:
            return True


def starts():
    newsTag = ["比特币, 区块链", "火链,火链财经", "行情", "深度", "应用"]
    for newsText in newsTag:
        n = 1
        while True:
            # 进行翻页
            data = {
                "page": str(n),
                "newsTag": newsText,
                "firstRowDate": "",
            }
            url = "https://api.huolian.online/nit/news/indexNewsListForPc"
            reponse = requests.post(url, data=data, headers=headers)
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                data = findNumber(html)
                n += 1
                if data:
                    break
            else:
                err = reponse.status_code
                mistake(url, err)
                break


if __name__ == '__main__':
    starts()