import requests
import json
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(text, month_day):
    dicts = {
        "_id": text["news_id"],
        "title": text["title"],
        "author": "蜂鸟财经--快讯",
        "release_time": "2018年" + month_day[0] + month_day[1] + text["time_hi"],
        "source": "蜂鸟财经：http://fengniaocaijing.com/",
        "main": text["content"],
    }
    storageDatabase(dicts, come_from="fengniaocaijing_alerts")


def download(reponse):
    html = reponse.text
    texts = json.loads(html)
    data = texts["data"]
    for text in data:
        print("fengniaocaijing_alerts")
        number = text["news_id"]
        if rechecking(number, come_from="fengniaocaijing_alerts"):
            break
        month_day = text["time_ymd"].split()[1:]
        storage(text, month_day)


def starts():
    reload = 0
    while True:
        url = "http://fengniaocaijing.com/api/route/news/news-flash/records?"
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            download(reponse)
            break
        else:
            if reload == 3:
                err = reponse.status_code
                mistake(url, err)
                break
            reload += 1


if __name__ == '__main__':
    starts()