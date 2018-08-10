import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, title_find


def storage(title, author, timeout, accurate, source, text):
    times = accurate + "  " + timeout
    dicts = {
        "title": title,
        "author": author,
        "release_time": times,
        "source": source,
        "main": text,
    }
    storageDatabase(dicts, come_from="tuoniaox_alerts")


def divide(i):
    try:
        print("tuoniaox_alerts")
        # 将从网页中用正则匹配到的局部html内容，变为xml格式的文档
        html = etree.HTML(i)
        # 获取实时的发布时间
        timeout = html.xpath('//span/text()')[0]
        # 获取信息的内容
        texts = html.xpath('//p/text()')[0].split()
        text = ""
        for i in texts:
            text += i + " "
        # 分离出标题以及其发布的时间日期
        pattern = re.compile("【[\s\S]*?】")
        title = re.findall(pattern, text)[0]
        # 由于没有明确的id值
        if title_find(title, come_from="tuoniaox_alerts"):
            return
        pattern = re.compile("\d月\d日")
        accurate = re.findall(pattern, text)
        if accurate:
            accurate = accurate[0]
        else:
            accurate = ""
        author = "鸵鸟区块链：https://www.tuoniaox.com/"
        # 判断是否是该网站的原创作
        source = html.xpath('//a/@href')
        if source:
            source = "负责编译--原文：" + source
        else:
            source = "鸵鸟区块链--快讯"
        storage(title, author, timeout, accurate, source, text)
    except Exception as err:
        mistake(url="https://www.tuoniaox.com/", err=err)


def download(reponse, url):
    # 由于快讯信息没有分网页，也没有详情页
    html = reponse.text
    # 获取快讯的板块
    pattern = re.compile("<ul>[\s\S]*?</ul>")
    texts = re.findall(pattern, html)[0]
    pattern = re.compile("<li>[\s\S]*?</li>")
    text = re.findall(pattern, texts)
    for i in text:
        divide(i)


def starts():
    reload = 0
    while True:
        url = "https://www.tuoniaox.com/"
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            download(reponse, url)
            break
        else:
            if reload == 3:
                err = reponse.status_code
                mistake(url, err)
                break
            reload += 1

if __name__ == '__main__':
    starts()