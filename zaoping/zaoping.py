import re
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, text, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": "早评财经",
        "main": text,
        "img": img,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="zaoping")


def download(reponse, number):
    html = etree.HTML(reponse.text)
    data = html.xpath('/html/body/div[3]/div/div[1]/div')
    if not data:
        return True
    texts = etree.tostring(data[0], method="text", encoding="utf8").decode("utf8").split()
    # 获取标题
    title = texts[0]
    # 获取文章作者
    author = texts[1]
    # 获取发布时间
    timeout = texts[2] + " " + texts[3]
    # 文章的内容分布有两部分
    text = texts[6:]
    # 获取文章使用的图片地址
    img_p = html.xpath('/html/body/div[3]/div/div[1]/div/p/img/@src')
    img_a = html.xpath('/html/body/div[3]/div/div[1]/div/p/a/img/@src')
    img = img_p + img_a
    storage(number, title, author, timeout, text, img)


def connect(url, reload):
    # 进行连接
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf8"
    if reponse.status_code == 200:
        pattern_num = re.compile("\d+")
        number = re.findall(pattern_num, url)[0]
        if rechecking(number, come_from="zaoping"):
            # 新闻信息没有顺序规律，进行3次判断，如果连续3次就结束运行
            if reload == 3:
                return "end"
            else:
                reload += 1
                return "continue"
        print("zaoping")
        download(reponse, number)
    else:
        err = reponse.status_code
        mistake(url, err)
        return "end"


def getUrl(html):
    # 进行匹配分割筛选
    pattern = re.compile('<div class="article-main">[\s\S]*?<!---->')
    texts = re.findall(pattern, html)[0]
    pattern_url = re.compile('/article/\d+/\d+\.html')
    urls = re.findall(pattern_url, texts)
    urls = list(set(urls))
    reload = 0
    for i in urls:
        url = "http://zaoping.net" + i
        data = connect(url, reload)
        if data == "end":
            return "end"
        elif data == "continue":
            continue


def starts():
    n = 1
    while True:
        url = 'http://zaoping.net/list/7.html?page=%s&ids=zx' % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            # 从网页中获取新闻详情页的网址
            data = getUrl(html)
            if data == "end":
                break
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()