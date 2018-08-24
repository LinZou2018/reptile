import json
import headers
import requests
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(text):
    dicts = {
        "_id": text["id"],
        "title": text["title"],
        "release_time": text["publish_time"],
        "author": "链世界--快讯",
        "source": "链世界",
        "main": text["content"],
    }
    storageDatabase(dicts, come_from="lianshijie7234_alerts")


def download(text):
    storage(text)


def segmentation(html):
    texts = json.loads(html)
    data = texts["data"]
    data = data["data"]
    for text in data:
        number = text["id"]
        if rechecking(number, come_from="lianshijie7234_alerts"):
            return "end"
        print("lianshijie7234_alerts")
        download(text)
    timeout = data[-1]["publish_time"]
    return timeout


def starts():
    timeout = ""
    while True:
        url = "https://k.7234.cn/api/news/search?keyword=&up_time=" + timeout
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            data = segmentation(html)
            if data == "end":
                break
            else:
                timeout = data
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()