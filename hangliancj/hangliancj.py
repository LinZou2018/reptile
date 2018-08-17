import requests
from lxml import etree
import re
import headers
import time
from error_document import mistake
from mongodb_news import storageDatabase, max_id


def storage(number, title, author, timeout, text, label, statement, img):
    dicts = {
        "_id": number,
        "title": title,
        "release_time": timeout,
        "author": author,
        "source": "杭链财经",
        "main": text,
        "statement": statement,
        "label": label,
        "img": img,
    }
    storageDatabase(dicts, come_from="hangliancj")

def download(url, reponse, number):
    try:
        html = etree.HTML(reponse.text)
        # 获取到发布时间及其作者
        lists = html.xpath('/html/body/div[4]/div/div[1]/div/div[1]/div[2]/text()')
        pattern = re.compile("时间")
        timeout = re.findall(pattern, lists[0])
        if not timeout:
            author = lists[0]
            timeout = lists[1]
            label = lists[2]
        else:
            author = "杭链财经"
            timeout = lists[0]
            label = lists[1]
        pattern = re.compile('快讯')
        classify = re.findall(pattern, label)
        if classify:
            return
        # 判断发布时间以判断该编号的网址是否以在启用
        if timeout == "时间：1970-01-01":
            return True
        print("hangliancj")
        # 获取标题
        title = html.xpath('/html/body/div[4]/div/div[1]/div/div[1]/div[1]/text()')[0]
        # 获取文本内容
        texts = html.xpath('/html/body/div[4]/div/div[1]/div/div[1]/div[4]')[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        # 文章的声明
        statement = html.xpath('/html/body/div[4]/div/div[1]/div/div[1]/div[5]')[0]
        statement = etree.tostring(statement, method="text", encoding="utf8").decode("utf8").split()
        img = html.xpath('/html/body/div[4]/div/div[1]/div/div[1]/div[4]//img/@src')
        storage(number, title, author, timeout, text, label, statement, img)
    except Exception as err:
        mistake(url, err)
        return True


def starts():
    # 由于快讯网址上的快讯信息不是顺序排列，是乱序排列，采用已有的编号来爬取
    n = 8300
    tf = True
    # 判断数据库是否已经存在内容
    number = max_id(come_from="hangliancj")
    if number:
        n = number + 1
        tf = False
    while True:
        try:
            url = "http://hangliancj.com/article/%s.html" % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                data = download(url, reponse, n)
                if data:
                    break
            else:
                err = reponse.status_code
                mistake(url, err)
                break
            # 主要是运行的第一次
            if tf:
                n -= 1
            else:
                n += 1
        except TimeoutError:
            time.sleep(10)


if __name__ == '__main__':
    starts()