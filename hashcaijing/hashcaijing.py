import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, author, source, text):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": text,
    }
    storageDatabase(dicts, come_from="hashcaijing")


def download(url, number):
    print('hashcaijing')
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    # 判断网页是否加载成功
    if reponse.status_code == 200:
        try:
            # 获取标题、发布时间、作者、来源
            html = etree.HTML(reponse.text)
            title = html.xpath('/html/body/div[2]/div[1]/div/div[1]/ul/li[1]/b/text()')[0]
            if not len(title):
                return True
            timeout = html.xpath('/html/body/div[2]/div[1]/div/div[1]/ul/li[2]/i[1]/text()')[0]
            author = html.xpath('/html/body/div[2]/div[1]/div/div[1]/ul/li[2]/i[2]/text()')[0]
            source = "哈希财经" + ":" + url
            texts = html.xpath('//div[@class="contentNews"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            storage(number, title, timeout, author, source, text)
        except Exception as err:
            mistake(url, err)
    else:
        err = reponse.status_code
        mistake(url, err)


def getUrl(reponse):
    # 获取新闻网页的网址
    html = etree.HTML(reponse.text)
    urls = html.xpath('/html/body/div[2]/div[2]/div[2]/div/ul/li/a/@href')
    for i in urls:
        url = "http://www.hashcaijing.com" + i
        pattern = re.compile('\d+')
        # 判断数据库中是否已经下载过
        number = re.findall(pattern, url)[0]
        if rechecking(number, come_from="hashcaijing"):
            break
        download(url, number)
    pattern = re.compile('\d+')
    num = re.findall(pattern, urls[-1])[0]
    # 第一次爬取时获取更多的新闻信息
    num = int(num)
    while True:
        num -= 1
        if rechecking(num, come_from="hashcaijing"):
            break
        url = 'http://www.hashcaijing.com/Index/article/id/%s' % num
        if download(url, num):
            break


def starts():
    url = "http://www.hashcaijing.com"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    # 判断网页是否加载完成
    if reponse.status_code == 200:
        getUrl(reponse)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()