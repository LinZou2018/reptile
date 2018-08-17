import requests
import re
from lxml import etree
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, author, takeaway, label, texts, img, statement):
    dicts = {
        "_id": number,
        "title": title,
        "release_time": timeout,
        "author": author,
        "takeaway": takeaway,
        "label": label,
        "source": "火球财经",
        "main": texts,
        "statement": statement,
        "img": img,
    }
    storageDatabase(dicts, come_from="ihuoqiu")


def download(url, number):
    try:
        print("ihuoqiu")
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            # 获取标题
            title = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/p[1]/text()')[0]
            # 文章的发布时间
            timeout = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/p[2]/span[1]/text()')[0]
            # 对文章的标签
            label = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/p[2]/span[2]/span/text()')[0]
            # 导读
            takeaway = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/p/text()')[0]
            # 文章的作者
            author = html.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/p[1]/text()')[0]
            # 声明
            statement = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/p/span/text()')[0]
            # 文本
            texts = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div/p/text()')
            # 文章中出现过的图片
            img = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div/p/img/@src')
            storage(number, title, timeout, author, takeaway, label, texts, img, statement)
        else:
            err = reponse.status_code
            mistake(url, err)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile('/Content/[^\s]*?data=[^\s]*?__2C__2C')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    for i in urls:
        pattern = re.compile('video')
        video = re.findall(pattern, i)
        if video:
            continue
        url = "https://ihuoqiu.com" + i
        pattern = re.compile('(/Content/[^\s]*?data=)([^\s]*?__2C__2C)')
        num = re.findall(pattern, url)[0]
        number = num[1]
        if rechecking(number, come_from="ihuoqiu"):
            continue
        download(url, number)


def starts():
    urls = ["https://ihuoqiu.com/Home/Index", "https://ihuoqiu.com/Home/information",
            "https://ihuoqiu.com/Home/encyclopedias"]
    for url in urls:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            getUrl(reponse)
        else:
            err = reponse.status_code
            mistake(url, err)


if __name__ == '__main__':
    starts()

