import requests
from lxml import etree
import re
import time
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, texts, label, img):
    dicts ={
        "_id": number,
        "title": title,
        "release_time": timeout,
        "author": author,
        "source": "coinvoice ：http://www.coinvoice.cn/",
        "main": texts,
        "statement": "免责声明：CoinVoice公众号文章仅为资讯传播用，不构成任何投资建议。",
        "label": label,
        "img": img,
    }
    storageDatabase(dicts, come_from="coinvoice")


def UTCTime(timeout):
    # 判断时间是多久之前的
    pattern = re.compile("天")
    day = re.findall(pattern, timeout)
    pattern = re.compile("时")
    hour = re.findall(pattern, timeout)
    pattern = re.compile("分")
    minute = re.findall(pattern, timeout)
    pattern = re.compile("刚")
    nows = re.findall(pattern, timeout)
    pattern = re.compile("\d+")
    num = re.findall(pattern, timeout)[0]
    # 获取当前时间
    nowTheTime = int(time.time())
    # 计算新闻的发布的时间
    if len(day):
        marjin = int(num) * 24 * 60 * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(hour):
        marjin = int(num) * 60 * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(minute):
        marjin = int(num) * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(nows):
        return time.asctime(time.localtime(time.time()))
    else:
        # 如果是精确的时间就返回此时间
        return timeout



def download(url, number):
    try:
        print("coinvoice")
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            # 获取标题
            title = html.xpath('//*[@id="post"]/section/div[1]/article/header/h1/text()')[0]
            # 获取作者及其网址
            author = html.xpath('//*[@id="post"]/section/div[1]/article/header/div[2]/a/span/text()')[0]
            author_url = html.xpath('//*[@id="post"]/section/div[1]/article/header/div[2]/a/@href')[0]
            author = author + " ：" + author_url
            # 获取时间，计算得到大概的准确时间
            timeout_hour = html.xpath('//*[@id="post"]/section/div[1]/article/header/div[1]/div/text()')[0]
            timeout = UTCTime(timeout_hour)
            # 获取文本及使用的图片
            texts = html.xpath('//*[@id="article-body"]/div[2]/p/text()')
            if not texts:
                texts = html.xpath('//*[@id="article-body"]/div[2]/div[1]/p/text()')
                img = html.xpath('//*[@id="article-body"]/div[2]/div[1]/p/img/@src')
            else:
                img = html.xpath('//*[@id="article-body"]/div[2]/p/img/@src')
            # 文章的标签
            label = html.xpath('//*[@id="post"]/section/div[1]/article/section/a/text()')
            storage(number, title, author, timeout, texts, label, img)
        else:
            err = reponse.status_code
            mistake(url, err)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile("[a-zA-z]+://[^\s]*\.html")
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    for url in urls:
        pattern = re.compile("\d+")
        number = re.findall(pattern, url)[0]
        if rechecking(number, come_from="coinvoice"):
            continue
        download(url, number)


def starts():
    url = 'http://www.coinvoice.cn/'
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        getUrl(reponse)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()