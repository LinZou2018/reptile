import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, content_source, texts, statement, img):
    dicts = {
        "id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "content_source": content_source,
        "main": texts,
        "statement": statement,
        "img": img,
        "source": "比特币之家",
    }
    # print(dicts)
    storageDatabase(dicts, come_from="btc798")


def download(html, number):
    print("btc798")
    # 获取白天，内容来源，发布时间，作者
    title = html.xpath('/html/body/main/div/div[3]/div[2]/div[1]/text()')[0]
    content_source = html.xpath('/html/body/main/div/div[3]/div[2]/div[2]/div[2]/text()')[0].split()
    if content_source:
        content_source = content_source[-1]
    else:
        content_source = "比特币之家  原创"
    timeout = html.xpath('/html/body/main/div/div[3]/div[2]/div[2]/div[1]/span/text()')[1]
    author = html.xpath('/html/body/main/div/div[4]/div[1]/div[1]/a[2]/text()')[0].split()[0]
    # 文章有声明
    statement = html.xpath('/html/body/main/div/div[3]/div[4]/text()')[0].split()[0]
    # 获取文章内容及其使用的图片
    text_object = html.xpath('/html/body/main/div/div[3]/div[3]/div[1]')[0]
    texts = etree.tostring(text_object, method="text", encoding="utf8").decode("utf8")
    img_p_span = html.xpath('/html/body/main/div/div[3]/div[3]/div[1]/p/span/span/img/@src')
    img_span = html.xpath('/html/body/main/div/div[3]/div[3]/div[1]/p/span/img/@src')
    img_p = html.xpath('/html/body/main/div/div[3]/div[3]/div[1]/p/img/@src')
    img = img_p + img_span + img_p_span
    storage(number, title, author, timeout, content_source, texts, statement, img)


def downURL(html):
    # 获取下一篇新闻网址
    url = html.xpath('/html/body/main/div/div[2]/div[3]/a/@href')[0]
    pattern = re.compile("\d+")
    number = re.findall(pattern, url)[0]
    return int(number)


def connect(number):
    while True:
        # 循环获取信息
        try:
            url = "http://www.btc798.com/articles/%s.html" % number
            if rechecking(number, come_from="btc798"):
                break
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
        except TimeoutError:
            time.sleep(10)
            continue
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            download(html, number)
            data = downURL(html)
            number = data
        else:
            err = reponse.status_code
            mistake(url, err)
            break


def getUrl(reponse):
    # 获取最新新闻网址
    html = reponse.text
    pattern = re.compile('/articles/\d+\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    num = []
    for url in urls:
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)[0]
        num.append(int(number))
    number = max(num)
    connect(number)


def starts():
    url = "http://www.btc798.com/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        getUrl(reponse)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()