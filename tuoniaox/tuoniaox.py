import requests
import re
import headers
import time
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, accurate_time, source, text, label, statement, responsibility, cooperation):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": accurate_time,
        "source": source,
        "main": text,
        "label": label,
        "statement": statement,
        "responsility": responsibility,
        "cooperatiopn": cooperation,
    }
    storageDatabase(dicts, come_from="tuoniaox")


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
        print("tuoniaox")
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            # 获取标题
            title = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/h1/text()')[0]
            # 获取作者的信息
            author = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/div[1]/ul/span[2]/text()')[0]
            # 获取时间，有可能是大概时间，需要精准确认
            timeout = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/div[1]/ul/span[1]/text()')[0]
            accurate_time = UTCTime(timeout)
            # 文章的来源
            source_name = html.xpath('/html/body/section[1]/div/div[1]/ol/li[1]/a/span/text()')[0]
            source_class = html.xpath('/html/body/section[1]/div/div[1]/ol/li[2]/a/span/text()')[0]
            source = source_name + "--" + source_class + "：" + url
            # 文章有声明、责任以及合作的信息
            statement = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/div[3]/p[1]/text()')[0]
            responsibility = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/div[3]/p[3]/text()')[0]
            cooperation = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/div[3]/p[2]/text()')[0]
            # 获取文章内容，
            texts = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/div[2]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            img = html.xpath('/html/body/section[1]/div/div[1]/div/div/div[1]/div[2]/p/img/@src')
            # 获取文章的标签
            labels = html.xpath("/html/body/section[1]/div/div[1]/div/div/div[1]/section")[0]
            label = etree.tostring(labels, method="text", encoding="utf8").decode("utf8").split()
            storage(number, title, author, accurate_time, source, text, label, statement, responsibility, cooperation)
        else:
            err = reponse.status_code
            mistake(url, err)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile('https://www.tuoniaox.com/[^\s]*\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    for url in urls:
        pattern = re.compile("\d+")
        number = re.findall(pattern, url)[0]
        if rechecking(number, come_from="tuoniaox"):
            continue
        download(url, number)


def starts():
    reload = 0
    url = "https://www.tuoniaox.com/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf8"
    if reponse.status_code == 200:
        getUrl(reponse)
    else:
        if reload == 3:
            err = reponse.status_code
            mistake(url, err)
        reload += 1


if __name__ == '__main__':
    starts()