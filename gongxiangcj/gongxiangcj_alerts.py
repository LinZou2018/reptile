import re
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, title_find


def storage(title, timeout, main):
    dicts = {
        "title": title,
        "release_time": timeout,
        "main": main,
        "author": "共享财经--快讯",
        "source": "共享财经",
    }
    storageDatabase(dicts, come_from="gongxiangcj_alerts")


def download(text, reload):
    # 将分割后的数据再进行分割获取数据
    title = text[0]
    if title == "马云：不支持比特币":
        title = text[0] + " " + text[1]
        main = text[2: -2]
    else:
        main = text[1: -2]
    if title_find(title, come_from="gongxiangcj_alerts"):
        if reload == 3:
            return True
        else:
            reload += 1
            return
    timeout = text[-2] + " " + text[-1]
    storage(title, timeout, main)


def segmentation(html, reload):
    print("gongxiangcj_alerts")
    # 没有详情页，所以获取所以数据进行分割
    html = etree.HTML(html)
    texts = html.xpath('/html/body/div/div[2]/div/div[1]/div/div')
    del texts[-1]
    for data in texts:
        text = etree.tostring(data, method="text", encoding="utf8").decode("utf8").split()
        mse = download(text, reload)
        if mse:
            return True


def starts():
    n = 1
    reload = 0
    while True:
        url = 'http://gongxiangcj.com/short_news?page=%s' % n
        reponse = requests.get(url, headers=headers .header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            data = segmentation(html, reload)
            if data:
                break
            n += 1
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()