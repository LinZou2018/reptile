import requests
import json
import headers
import re
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
    # print(dicts)
    storageDatabase(dicts, come_from="babifinance")


def download(reponse):
    try:
        print("babifinance")
        html = reponse.text
        texts = json.loads(html)
        for text in texts:
            number = text["id"]
            if rechecking(number, come_from="babifinance"):
                return True
            # 分离出所需要的信息
            data = text["content"].split()
            pattern = re.compile("来源")
            exist = re.findall(pattern, data[0])
            if exist:
                source = data[0]
                reload = -1
                while True:
                    statement = data[reload]
                    if statement != "&nbsp;":
                        statement = data[reload]
                        pattern = re.compile("作者")
                        exist = re.findall(pattern, data[0])
                        if exist:
                            author = data[0]
                            main = data[1: reload]
                            storage(author, source, statement, main, text)
                            break
                        else:
                            reload -= 1
                            author = data[reload]
                            while True:
                                if author != "&nbsp":
                                    pattern = re.compile('编辑|作者')
                                    exist = re.findall(pattern, author)
                                    if exist:
                                        if len(author) < 30:
                                            main = data[1: reload]
                                            storage(author, source, statement, main, text)
                                            break
                                        else:
                                            reload += 1
                                            author = "BABI财经"
                                            main = data[1: reload]
                                            storage(author, source, statement, main, text)
                                            break
                                    else:
                                        author = "BABI财经"
                                        reload += 1
                                        main = data[1: reload]
                                        storage(author, source, statement, main, text)
                                        break
                                else:
                                    reload -= 1
                            break
                    else:
                        reload -= 1
            else:
                source = "BABI财经"
                reload = -1
                while True:
                    statement = data[reload]
                    if statement != "&nbsp;":
                        statement = data[reload]
                        pattern = re.compile("作者")
                        exist = re.findall(pattern, data[0])
                        if exist:
                            author = exist[0]
                            main = data[1: reload]
                            storage(author, source, statement, main, text)
                            break
                        else:
                            reload -= 1
                            author = data[reload]
                            while True:
                                if author != "&nbsp":
                                    pattern = re.compile('编辑|作者')
                                    exist = re.findall(pattern, author)
                                    if exist:
                                        if len(author) < 30:
                                            main = data[1: reload]
                                            storage(author, source, statement, main, text)
                                            break
                                        else:
                                            reload += 1
                                            author = "BABI财经"
                                            main = data[1: reload]
                                            storage(author, source, statement, main, text)
                                            break
                                    else:
                                        author = "BABI财经"
                                        reload += 1
                                        main = data[: reload]
                                        storage(author, source, statement, main, text)
                                        break
                                else:
                                    reload -= 1
                            break
                    else:
                        reload -= 1
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
                data = download(reponse)
                n += 1
                if data:
                    break
            else:
                if reload == 3:
                    err = reponse.status_code
                    mistake(url, err)
                    break
                reload += 1


if __name__ == '__main__':
    starts()