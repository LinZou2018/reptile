import re
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, source, texts, label, classify, statement, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": texts,
        "label": label,
        "classify": classify,
        "statement": statement,
        "ing": img,
    }
    storageDatabase(dicts, come_from="epcnn_alerts")


def download(html, author, number, url):
    try:
        print("epcnn_alerts")
        # 获取标题
        title = html.xpath('/html/body/section/div[1]/div/header/h1/a/text()')[0]
        # 获取发布时间
        timeout = html.xpath('/html/body/section/div[1]/div/header/div/span[1]/text()')[0]
        # 文章的分类
        classify = html.xpath('/html/body/section/div[1]/div/header/div/span[2]/a/text()')[0]
        # 文章的标签
        label = html.xpath('/html/body/section/div[1]/div/div[5]/a/text()')
        # 本网站此文章的声明
        statement = html.xpath('/html/body/section/div[1]/div/div[3]/text()')[0]
        # 所引用到的图片
        img = html.xpath('/html/body/section/div[1]/div/article/p/img/@src')
        # 文章的来源位置
        source_location = html.xpath('/html/body/div[2]/div/a/text()')
        source = "e能链财经"
        for i in source_location:
            source += "-" + i
        # 文章的正文内容
        texts = html.xpath('/html/body/section/div[1]/div/article/p/text()')
        storage(number, title, author, timeout, source, texts, label, classify, statement, img)
    except Exception as err:
        mistake(url, err)


def getUrl(html):
    urls = html.xpath('/html/body/section/div[1]/div/article/header/h2/a/@href')
    # 获取文章对应的作者
    authors = html.xpath('/html/body/section/div[1]/div/article/p[1]/span[1]/text()')
    for url, author in zip(urls, authors):
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        # 文章对应的编号
        pattern = re.compile('\d+')
        number = re.findall(pattern, url)[0]
        if rechecking(number, come_from="epcnn_alerts"):
            return True
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            download(html, author, number, url)
        else:
            err  = reponse.status_code
            mistake(url, err)


def starts():
    n = 1
    while True:
        url = 'https://www.epcnn.com/sg/page/%s' % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            data = getUrl(html)
            if data:
                break
            n += 1
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()