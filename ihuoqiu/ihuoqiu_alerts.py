import requests
import time
from lxml import etree
import headers
from error_document import mistake
from mongodb_news import storageDatabase, title_find


def storage(title, timeout, main):
    dicts = {
        'title': title,
        "release_time": timeout,
        "author": "火球财经--快讯",
        "source": "火球财经",
        "main": main,
    }
    storageDatabase(dicts, come_from="ihuoqiu_alerts")


def download(reponse):
    print("ihuoqiu_alerts")
    html = etree.HTML(reponse.text)
    date = time.asctime(time.localtime(time.time())).split()
    texts = html.xpath('//*[@id="panel1"]/div')
    for i in texts:
        text = etree.tostring(i, method="text", encoding="utf8").decode("utf8").split()
        # 将时间调整好
        date[-2] = text[0]
        timeout = ""
        for da in date:
            timeout += da + " "
        title = text[1]
        if title_find(title, come_from="ihuoqiu_alerts"):
            break
        # 将正文组合好
        if text[-2] == "[查看原文]":
            main = text[2:-2]
        else:
            main = text[2:-1]
        storage(title, timeout, main)


def starts():
    url = 'https://ihuoqiu.com/Home/newsflash'
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        download(reponse)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()