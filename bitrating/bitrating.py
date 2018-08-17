import time
import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, compile_one, author_object, author_url, release_time, source, text, recommend):
    redact = ""
    for i in compile_one:
        redact += i + " "
    # 将作者及作者的网址还有编辑组合
    author = redact + " -- " + author_object + ":" + author_url
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": release_time,
        "source": source,
        "main": text,
        "recommend": recommend,
    }
    # 存入数据库
    storageDatabase(dicts, come_from="bitrating")


def UTCTime(timeout):
    # 判断时间是多久之前的
    pattern = re.compile("天")
    day = re.findall(pattern, timeout)
    pattern = re.compile("时")
    hour = re.findall(pattern, timeout)
    pattern = re.compile("分")
    minute = re.findall(pattern, timeout)
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
    else:
        # 如果是精确的时间就返回此时间
        return timeout


def download(number, url):
    print("bitrating")
    try:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "urf-8"
        # 判断网页是否加载成功
        if reponse.status_code == 200:
            try:
                html = etree.HTML(reponse.text)
                # 获取新闻的标题
                title = html.xpath('/html/body/section/div[2]/div/header/div[1]/h1/a/text()')[0]
                compile_object = html.xpath('//div[@class="small"]')[0]
                compile_one = etree.tostring(compile_object, method="text", encoding="utf8").decode("utf8").split()
                # 作者及作者的网址
                author_object = html.xpath('/html/body/section/div[2]/div/div[6]/h4/a/text()')[0]
                author_url = html.xpath('/html/body/section/div[2]/div/div[6]/h4/a/@href')[0]
                # 获取新闻的发布时间
                timeout = html.xpath('/html/body/section/div[2]/div/header/div[2]/span[1]/text()')[0]
                # 有的时间不精确，从新计算
                release_time = UTCTime(timeout)
                # 新闻的来源及网址
                source = "比特评级：" + url
                texts = html.xpath('//article[@class="article-content "]')[0]
                # 获取新闻的信息内容
                text = etree.tostring(texts, method='text', encoding="utf8").decode("utf8").split()
                # 新闻有推荐信息
                recommends = html.xpath('//div[@class="asb-post-footer"]')[0]
                recommend = etree.tostring(recommends, method="text", encoding="utf8").decode("utf")
                recommend += ": https://bitrating.com/wenda"
                storage(number, title, compile_one, author_object, author_url, release_time, source, text, recommend)
            except Exception as err:
                mistake(url, err)
        else:
            err = reponse.status_code
            mistake(url, err)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    # 获取新闻的网址
    pattern = re.compile('[a-zA-z]+://[^\s]*\.html')
    urls = re.findall(pattern, reponse.text)
    urls = list(set(urls))
    for url in urls:
        pattern_live = re.compile("live")
        num = re.findall(pattern_live, url)
        if not len(num):
            # 获取新闻所有的编号
            pattern_number = re.compile("\d+")
            number = re.findall(pattern_number, url)[0]
            # 判断在数据库是否已经下载过
            if rechecking(number, come_from="bitrating"):
                break
            download(number, url)


def starts():
    # 新闻来源的主要几个网址
    urls = ["https://bitrating.com/", "https://bitrating.com/bitcoin", "https://bitrating.com/blockchain"]
    for url in urls:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        # 判断网页是否加载成功
        if reponse.status_code == 200:
            getUrl(reponse)
        else:
            err = reponse.status_code
            mistake(url, err)

if __name__ == '__main__':
    starts()