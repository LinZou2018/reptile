import requests
import json
import headers
import time
from error_document import mistake
from mongodb_news import storageDatabase, rechecking, max_id


def storage(text, timeout):
    dicts = {
        "_id": text["id"],
        "title": text["title"],
        "authoe": "波罗财经--快讯",
        "release_time": timeout,
        "source": text["source"],
        "main": text["content"]
    }
    storageDatabase(dicts, come_from="polo321_alerts")


def download(text):
    timeout = text["sdate"] + "  " + text["stime"]
    storage(text, timeout)


def classify(reponse):
    print("polo321_alerts")
    html = reponse.text
    # 将json格式的文档转换为字典格式
    texts = json.loads(html)
    data = texts["data"]
    main_text = data[0]["list"]
    for text in main_text:
        number = text["id"]
        if rechecking(number, come_from="polo321_alerts"):
            return True
        download(text)


def starts():
    n = 8208
    tf = True
    # 判断数据库是否已经存在内容
    number = max_id(come_from="polo321_alerts")
    if number:
        n = number + 20
        tf = False
    while True:
        try:
            url = "http://39.108.117.97:8082/lives/getList?Id=%s&flag=down" % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                data = classify(reponse)
                if data:
                    break
            else:
                err = reponse.status_code
                mistake(url, err)
                break
            # 主要是运行的第一次
            if tf:
                n -= 20
            else:
                n += 20
        except TimeoutError:
            time.sleep(10)


if __name__ == '__main__':
    starts()