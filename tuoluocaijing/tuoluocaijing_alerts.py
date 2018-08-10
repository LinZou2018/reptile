import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, source, texts, label):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": texts,
        "label": label,
    }
    storageDatabase(dicts, come_from="tuoluocaijing_alerts")


def download(reponse, number, url):
    try:
        print("tuoluocaijing_alerts")
        html = etree.HTML(reponse.text)
        title = html.xpath("/html/body/div[6]/div[1]/div/h1/text()")[0]
        # 获取标题
        author = "陀螺快讯：" + "https://www.tuoluocaijing.cn/kuaixun"
        # 获取发布时间
        timeout = html.xpath("/html/body/div[6]/div[1]/div/div[1]/span/text()")[0]
        source = "陀螺财经--[快讯]：" + url
        # 有分类标签
        label = html.xpath("/html/body/div[5]/div/span/a[2]/text()")[0]
        # 获取正文，有两种情况
        texts = html.xpath("/html/body/div[6]/div[1]/div/div[2]/blockquote/text()")[0].split()
        if not texts:
            texts = html.xpath("/html/body/div[6]/div[1]/div/div[2]/blockquote/p/text()")
        storage(number, title, author, timeout, source, texts, label)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    pattern = re.compile('/kuaixun/detail-\d+\.html')
    urls = re.findall(pattern, reponse.text)
    urls = list(set(urls))
    for i in urls:
        reload = 0
        try:
            url = "https://www.tuoluocaijing.cn" + i
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                pattern_num = re.compile("\d+")
                number = re.findall(pattern_num, url)[0]
                if rechecking(number, come_from="tuoluocaijing_alerts"):
                    break
                download(reponse, number, url)
            else:
                err = reponse.status_code
                mistake(url, err)
                if reload == 3:
                    break
                reload += 1
        except:
            if reload == 3:
                break
            reload += 1


def starts():
    n = 1
    reload = 0
    while True:
        try:
            url = "https://www.tuoluocaijing.cn/kuaixun/page-%s.html" % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                getUrl(reponse)
                n += 1
            else:
                if reload == 3:
                    err = reponse.status_code
                    mistake(url, err)
                    break
                reload += 1
        except:
            if reload == 3:
                break
            reload += 1


if __name__ == '__main__':
    starts()