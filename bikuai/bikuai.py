import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, takeaway, statement, text, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "timeout": timeout,
        "takeaway": takeaway,
        "main": text,
        "source": "币块财经",
        "statement":statement,
        "img": img,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="bikuai")


def download(html, number):
    print("bikuai")
    # 获取标题、作者、发布时间
    title = html.xpath('/html/body/div[3]/div/div[1]/div/div[1]/h1/text()')[0]
    author = html.xpath('/html/body/div[3]/div/div[1]/div/div[2]/div[1]/a[2]/text()')[0]
    timeout = html.xpath('/html/body/div[3]/div/div[1]/div/div[2]/div[2]/span[1]/text()')[0]
    # 文章的导读及声明
    takeaway = html.xpath('/html/body/div[3]/div/div[1]/div/div[3]/text()')[0].split()[0]
    statement = html.xpath('/html/body/div[3]/div/div[1]/div/div[5]/text()')[0].split()[0]
    # 文章的内容和使用过的图片
    texts = html.xpath('/html/body/div[3]/div/div[1]/div/div[4]')[0]
    text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
    img = html.xpath('/html/body/div[3]/div/div[1]/div/div[4]/p/img/@src')
    storage(number, title, author, timeout, takeaway, statement, text, img)


def downURL(html):
    url_hind = html.xpath('/html/body/div[3]/div/div[1]/div/div[6]/div[2]/a/@href')[0]
    url = "http://www.bikuai.org" + url_hind
    return url


def connect(number):
    url = "http://www.bikuai.org/news/%s.html" % number
    while True:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            download(html, number)
            data = downURL(html)
            url = data
            pattern_num = re.compile('\d+')
            number = int(re.findall(pattern_num, url)[0])
            if rechecking(number, come_from="bikuai"):
                break
        else:
            err = reponse.status_code
            mistake(url, err)
            break


def getUrl(html):
    pattern = re.compile('/\d+\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    num = []
    for i in urls:
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, i)[0]
        num.append(int(number))
    number = max(num)
    connect(number)


def starts():
    url = "http://www.bikuai.org"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        getUrl(html)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()