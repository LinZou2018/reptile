import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, max_id


def storage(number, title, timeout, content_source, texts, label, statement, img):
    print("chainfor")
    dicts = {
        "_id": number,
        "title": title,
        "release_time": timeout,
        "author": "链向财经编辑",
        "source": "链向财经",
        "content_source": content_source,
        "main": texts,
        "label": label,
        "statement": statement,
        "img": img,
    }
    storageDatabase(dicts, come_from="chainfor")


def UTCTime(timeout):
    # 判断时间是多久之前的
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
    if len(hour):
        marjin = int(num) * 60 * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(minute):
        marjin = int(num) * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(nows):
        return time.asctime(time.localtime(time.time()))
    elif len(timeout.split()) == 2:
        return timeout
    else:
        # 如果是精确的时间就返回此时间
        date = time.localtime()
        timeout = date.tm_year + "-" + date.tm_mon + "-" + date.tm_mday + " " + timeout
        return timeout


def download(html, number):
    try:
        html = etree.HTML(html)
        # 获取标题
        title = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/h1/text()')[0]
        # 获取时间，在加以更正
        timeout = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[1]/p[1]/span/text()')[0]
        timeout = UTCTime(timeout)
        # 文章的标签
        label = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[1]/p[2]/span/text()')[0]
        # 文章的内容来源
        content_source = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[1]/p[3]/span/text()')[0].split()[0]
        # 文章的声明
        statement = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/p[1]')[0]
        statement = etree.tostring(statement, method="text", encoding="utf8").decode("utf8").split()[0]
        # 文章的内容和使用的图片
        texts = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[2]/p/text()')
        img = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div[1]/div[2]/p/img/@src')
        storage(number, title, timeout, content_source, texts, label, statement, img)
    except:
        return "continue"


def getUrl(reponse, tf, url):
    # 网址加载成功进行获取信息
    html = reponse.text
    pattern = re.compile('\d+')
    number = re.findall(pattern, url)[0]
    data = download(html, number)
    if data == "continue":
        return data
    # 获取上或者下一篇的url
    pattern_text_url = re.compile('<div class="m-i-page">[\s\S]*?</div>')
    text_url = re.findall(pattern_text_url, html)[0]
    pattern_url = re.compile('[a-zA-z]+://[^\s]*\.html')
    urls = re.findall(pattern_url, text_url)
    # 进行判断本篇文章是否是最后一篇文章
    if len(urls) == 1:
        return "end"
    # 判断是去返回上一篇的URL还是下一篇的url，主要是第一次爬取信息时，需要在运行结束后再运行一次
    if tf:
        url_up = urls[0]
        if url_up:
            return url_up
        else:
            return "end"
    else:
        url_down = urls[1]
        if url_down:
            return url_down
        else:
            return "end"


def starts():
    n = 33588
    # 用与判断获取路径是获取上一篇还是下一篇
    tf = True
    # 判断数据库是否已经存在内容
    number = max_id(come_from="chainfor")
    if number:
        n = int(number) + 1
        tf = False
    url = "https://www.chainfor.com/news/show/%s.html" % n
    while True:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            data = getUrl(reponse, tf, url)
            if data == "end":
                break
            elif data == "continue":
                continue
            # 返回路径，跟新
            url = data
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()