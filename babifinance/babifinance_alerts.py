import requests
import headers
import json
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(text):
    dicts = {
        "_id": text["id"],
        "title": text["title"],
        "author": text["username"],
        "release_time": text["updatetime"],
        "main": text["content"],
        "source": "BABI财经：" + text["url"],
    }
    storageDatabase(dicts, come_from="babifinance_alerts")


def download(reponse):
    print("babifinance_alerts")
    html = reponse.text
    # 将文本转换为字典格式数据
    texts = json.loads(html)
    for text in texts:
        number = text["id"]
        if rechecking(number, come_from="babifinance_alerts"):
            break
        storage(text)


def starts():
    n = 1
    reload = 0
    while True:
        url = 'http://www.babifinance.com/api.php?op=autoload&siteid=1&modelid=12&catid=7&pagesize=10&page=%s' % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            download(reponse)
            n += 1
            reload = 0
        else:
            if reload == 3:
                err = reponse.status_code
                mistake(url, err)
                break
            reload += 1


if __name__ == '__main__':
    starts()