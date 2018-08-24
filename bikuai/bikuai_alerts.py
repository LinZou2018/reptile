import time
import json
# import headers
import requests
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Length": "6",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "www.bikuai.org",
    "Origin": "http://www.bikuai.org",
    "Referer": "http://www.bikuai.org/kuaibao.php",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def storage(text):
    dicts = {
        "_id": text["id"],
        "title": text["title"],
        "author": "币块财经--快讯",
        "release_time": text["time1"] + " " + text["time2"],
        "main": text["body"],
        "source": "币块财经",
    }
    storageDatabase(dicts, come_from="bikuai_alerts")


def download(reponse):
    # 获取的文本字典化
    print("bikuai_alerts")
    html = reponse.text
    data = json.loads(html)
    for text in data:
        number = text["id"]
        if rechecking(number, come_from="bikuai_alerts"):
            return True
        storage(text)


def stars():
    n = 0
    while True:
        data = {
            "page": str(n),
        }
        try:
            url = "http://www.bikuai.org/kuaibao.php"
            reponse = requests.post(url, data=data, headers=headers)
        except TimeoutError:
            # 如果是网络连接超时，则就等待10秒从新加载
            time.sleep(10)
            continue
        reponse.encoding = "urf-8"
        if reponse.status_code == 200:
            data = download(reponse)
            if data:
                break
            n += 1
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    stars()