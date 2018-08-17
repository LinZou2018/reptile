import requests
import json
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, timeout, text):
    dicts = {
        "_id": number,
        "title": text["title"],
        "author": "币源社区--快讯",
        "release_time": timeout,
        "source": text["source"],
        "main": text["content"],
    }
    storageDatabase(dicts, come_from="coingogo_alerts")


def download(reponse):
    print("coingogo_alerts")
    html = reponse.text
    data = json.loads(html)
    texts = data["list"]
    for text in texts:
        number = text["id"]
        if rechecking(number, come_from="coingogo_alerts"):
            return True
        createtime = text["createtime"]
        timeout = str(createtime["year"]) + "年" + str(createtime["mon"]) + "月" + str(createtime["mday"]) + "日  " + str(createtime["hours"]) + ":" + str(createtime["minutes"]) + "  " + createtime["weekday"]
        storage(number, timeout, text)


def starts():
    n = 1
    while True:
        url = 'http://www.coingogo.com/flash/default/list?type=2&page=%s&title=' % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            data = download(reponse)
            if data:
                break
            n += 1
        else:
            err = reponse.status_code
            mistake(url, err)


if __name__ == '__main__':
    starts()