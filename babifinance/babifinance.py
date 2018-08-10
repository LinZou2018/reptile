import requests
import json
import headers
import time
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(author, source, statement, main, text):
    dicts = {
        "_id": text["id"],
        "title": text["title"],
        "author": author,
        "release_time": text["updatetime"],
        "main": main,
        "source": source,
        "statement": statement,
        "img": text["thumb"],
    }
    storageDatabase(dicts, come_from="babifinance")


def download(reponse):
    try:
        print("babifinance")
        html = reponse.text
        texts = json.loads(html)
        for text in texts:
            number = text["id"]
            if rechecking(number, come_from="babifinance"):
                break
            # 分离出所需要的信息
            source = text["content"].split()[0]
            author = text["content"].split()[-2]
            if author == "&nbsp;":
                author = text["content"].split()[-3]
            statement = text["content"].split()[-1]
            main = text["content"].split()[1: -2]
            if author == "&nbsp;":
                main = text["content"].split()[1: -3]
            storage(author, source, statement, main, text)
    except Exception as err:
        mistake(url="http://www.babifinance.com/", err=err)


def starts():
    # 数据的来源地址
    urls = ["http://www.babifinance.com/api.php?op=autoload&siteid=1&modelid=1&catid=6&pagesize=10&page=%s",
            "http://www.babifinance.com/api.php?op=autoload&siteid=1&modelid=1&catid=9&pagesize=10&page=%s",
            "http://www.babifinance.com/api.php?op=autoload&siteid=1&modelid=1&catid=17&pagesize=10&page=%s"]
    for i in urls:
        n = 1
        reload = 0
        while True:
            url = i % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                download(reponse)
                n += 1
            else:
                if reload == 3:
                    err = reponse.status_code
                    mistake(url, err)
                    break
                reload += 1


if __name__ == '__main__':
    starts()