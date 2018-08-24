import re
import json
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(text, timeout, title_text, title):
    dicts = {
        "_id": text["id"],
        "title": title,
        "author": "链向财经--快讯",
        "release_time": timeout,
        "main": title_text,
        "source": "链向财经",
    }
    # print(dicts)
    storageDatabase(dicts, come_from="chainfor_alerts")


def download(text):
    timeout_obj = text["createDate"]["time"]
    timeout = time.asctime(time.localtime(int(timeout_obj)/1000))
    title_text = text["introduction"]
    pattern = re.compile('【[\s\S]*?】')
    title = re.findall(pattern, title_text)
    storage(text, timeout, title_text, title)

def connent(html):
    print("chainfor_alerts")
    data = json.loads(html)
    obj = data["obj"]
    texts = obj["list"]
    for text in texts:
        number = text["id"]
        if rechecking(number, come_from="chainfor_alerts"):
            return True
        download(text)


def starts():
    n = 1
    while True:
        url = "https://www.chainfor.com/news/list/flashnew/data.do?type=0&pageSize=15&pageNo=%s&title=" % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            data = connent(html)
            n += 1
            if data:
                break
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()