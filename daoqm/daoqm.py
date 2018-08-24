import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, content_source, text, statement, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "content_source": content_source,
        "main": text,
        "statement": statement,
        "source": "链易财经",
        "img": img,
    }
    storageDatabase(dicts, come_from="daoqm")


def download(html, number):
    print("daoqm")
    # 信息进行页面更改
    if int(number) > 230:
        # 获取标题、作者、来源、发布时间
        title = html.xpath('//*[@id="Article"]/h1/text()')[0]
        time_author_source = html.xpath('//*[@id="Article"]/div[1]/text()')[0].split()
        author = time_author_source[3]
        timeout = time_author_source[0] + " " + time_author_source[1]
        content_source = time_author_source[2]
        # 文章有声明
        statement = html.xpath('//*[@id="state"]/p/text()')[0]
        texts = html.xpath('//*[@id="Article"]/div[2]')[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        # 获取使用过的图片
        img_p = html.xpath('//*[@id="Article"]/div[2]/p/img/@src')
        img_span = html.xpath('//*[@id="Article"]/div[2]/p/span/img/@src')
        img = img_span + img_p
        storage(number, title, author, timeout, content_source, text, statement, img)
    else:
        return True



def downURL(html):
    # 获取上一篇内容时分类
    url = html.xpath('//*[@id="Article"]/p/a[1]/@href')[0]
    return url


def connect(url):
    # 循环获取网页
    while True:
        pattern = re.compile('\d+')
        number = re.findall(pattern, url)[0]
        if rechecking(number, come_from="daoqm"):
            break
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            data = download(html, number)
            if data:
                break
            data = downURL(html)
            url = data
        else:
            err = reponse.status_code
            mistake(url, err)
            break


def getURL(html, url):
    # 获取最新的网页地址
    pattern = re.compile('https://[^\s]*\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    num = []
    for i in urls:
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, i)[0]
        num.append(int(number))
    number = max(num)
    url = url + str(number) + ".html"
    connect(url)


def starts():
    urls = ["https://www.daoqm.com/news/", "https://www.daoqm.com/industry/", "https://www.daoqm.com/activity/",
            "https://www.daoqm.com/deve/"]
    for url in urls:
        try:
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
        except TimeoutError:
            time.sleep(10)
            continue
        if reponse.status_code == 200:
            html = reponse.text
            getURL(html, url)
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()