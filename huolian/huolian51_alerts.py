import json
import requests
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "7",
    "Content-Type": "application/x-www-form-urlencoded",
    "deviceType": "H5",
    "Host": "api.huolian.online",
    "nitToken": "",
    "Origin": "https://huolian.com",
    "Referer": "https://huolian.com/fire.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
}


def storage(text):
    dicts = {
        "_id": text["informationId"],
        "title": text["title"],
        "author": text["authorUser"],
        "release_time": text["insertDate"],
        "source": "火链财经--快讯",
        "main": text["content"],
    }
    storageDatabase(dicts, come_from="huolian_alerts")


def download(html):
    print("51huolian_alerts")
    html = json.loads(html)
    data = html["data"]
    for text in data:
        number = text["informationId"]
        if rechecking(number, come_from="huolian_alerts"):
            return True
        storage(text)


def starts():
    n = 1
    while True:
        # 进行翻页
        data = {
            "page": str(n),
        }
        url = "https://api.huolian.online/nit/information/informationListForPc"
        reponse = requests.post(url, data=data, headers=headers)
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            data = download(html)
            if data:
                break
            n += 1
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()