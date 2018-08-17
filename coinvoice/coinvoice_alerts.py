import requests
from lxml import etree
import re
import headers
import time
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, main_text):
    dicts = {
        "_id": number,
        "title": title,
        "author": "coinvoice--快讯",
        "timeout": timeout,
        "main": main_text,
        "source": "coinvoice：http://www.coinvoice.cn"
    }
    storageDatabase(dicts, come_from="coinvoice_alerts")

def UTCTime(timeout):
    # 判断时间是多久之前的
    pattern = re.compile("d")
    day = re.findall(pattern, timeout)
    pattern = re.compile("h")
    hour = re.findall(pattern, timeout)
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
    else:
        # 如果是精确的时间就返回此时间
        return timeout


def download(text):
    try:
        print("coinvoice_alerts")
        text = etree.HTML(text)
        number = text.xpath('//div[@class="date"]/@data-time')[0]
        if rechecking(number, come_from="coinvoice_alerts"):
            return True
        title = text.xpath('//div[@class="title"]/text()')[0]
        # 时间不够精确
        timeout = text.xpath('//div[@class="date"]/text()')[0]
        timeout_new = UTCTime(timeout)
        timeout = timeout_new + " --- " + timeout + "前左右"
        # 获取正文
        main_text = text.xpath('//div[@class="summary"]/text()')[0]
        storage(number, title, timeout, main_text)
    except Exception as err:
        mistake(url="http://www.coinvoice.cn/category/kuaixun", err=err)


def getText(reponse):
    html = reponse.text
    # 获取所有快讯的对象
    pattern = re.compile('<div class="flash-item">[\s\S]*?</div></div></div>')
    texts = re.findall(pattern, html)
    for text in texts:
        data = download(text)
        if data:
            break


def starts():
    url = 'http://www.coinvoice.cn/category/kuaixun'
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        getText(reponse)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()