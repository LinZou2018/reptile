import re
import json
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, content_source, main_text, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "content_source": content_source,
        "main": main_text,
        "source": "共享财经",
        "img": img,
    }
    storageDatabase(dicts, come_from="gongxiangcj")


def download(html, title, timeout, author, number):
    print("gongxiangcj")
    # 进行数据处理
    html = etree.HTML(html)
    text = html.xpath('/html/body/div/div[2]/div[2]/div/div[2]')[0]
    text = etree.tostring(text, method="text", encoding="utf8").decode("utf8").split()
    if not text:
        return "continue"
    # 判断是否有源文链接
    pattern = re.compile('原文：')
    exist = re.findall(pattern, text[0])
    if exist:
        pattern_sos = re.compile('([\s\S]*?)(原文：)([\s\S]*)')
        data = re.findall(pattern_sos, text[0])
        content_source = data[1] + data[2]
        main_text = data[0]
    else:
        main_text = text[0]
        content_source = "共享财经原创"
    img = html.xpath('/html/body/div/div[2]/div[2]/div/div[2]/p/img/@src')
    storage(number, title, author, timeout, content_source, main_text, img)


def connect(text, number):
    # 连接新闻的详情页
    url = "http://gongxiangcj.com/posts/%s" % number
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        title = text["title"]
        timeout = text["date"]
        author = text["username"]
        html = reponse.text
        data = download(html, title, timeout, author, number)
        if data == "continue":
            return "continue"
    else:
        err = reponse.status_code
        mistake(url, err)
        return "end"


def getUrl(html):
    # 获取数据转换为字典格式
    data = json.loads(html)
    posts = data["posts"]
    for text in posts:
        # 获得新闻的编号
        number = text["id"]
        if rechecking(number, come_from="gongxiangcj"):
            return True
        data = connect(text, number)
        if data == "continue":
            continue
        elif data == "end":
            return True


def starts():
    urls = ["http://gongxiangcj.com/get_posts?page=%s&post_type=", "http://gongxiangcj.com/get_posts?page=%s&post_type=1",
            "http://gongxiangcj.com/get_posts?page=%s&post_type=2", "http://gongxiangcj.com/get_posts?page=%s&post_type=3",
            "http://gongxiangcj.com/get_posts?page=%s&post_type=4", "http://gongxiangcj.com/get_posts?page=%s&post_type=5",
            "http://gongxiangcj.com/get_posts?page=%s&post_type=6", "http://gongxiangcj.com/get_posts?page=%s&post_type=7"]
    for i in urls:
        n = 1
        while True:
            # 对网页进行翻页处理
            url = i % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                data = getUrl(html)
                if data:
                    break
            else:
                err = reponse.status_code
                mistake(url, err)
                break


if __name__ == '__main__':
    starts()