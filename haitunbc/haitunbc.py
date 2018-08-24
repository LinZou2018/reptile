import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, content_source, text, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": "海豚区块链",
        "content_source": content_source,
        "main": text,
        "img": img,
    }
    storageDatabase(dicts, come_from="haitunbc")


def download(reponse, number, url):
    try:
        print("haitunbc")
        html = etree.HTML(reponse.text)
        # 获取标题
        title = html.xpath('//*[@id="layer8A0AB3AA964FD517CD3E813B876C3806"]/div/div[1]/text()')[0]
        # 文章其内容来源
        content_source = html.xpath('//*[@id="layer8A0AB3AA964FD517CD3E813B876C3806"]/div/div[2]/div/span[1]/text()')[0]
        # 获取作者
        author = html.xpath('//*[@id="layer8A0AB3AA964FD517CD3E813B876C3806"]/div/div[2]/div/span[3]/text()')[0]
        # 获取发布时间
        timeout = html.xpath('//*[@id="layer8A0AB3AA964FD517CD3E813B876C3806"]/div/div[2]/div/span[5]/text()')[0]
        # 获取文章的正文
        texts = html.xpath('//*[@id="layer8A0AB3AA964FD517CD3E813B876C3806"]/div/div[4]/div')[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        if not text:
            texts = html.xpath('//div[@class="artview_content"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        num = text.index('推荐公众号：币萌主')
        text = text[:num]
        # 文章中使用过的图片
        img = html.xpath('//*[@id="layer8A0AB3AA964FD517CD3E813B876C3806"]/div/div[4]/div//img/@src')[:-2]
        storage(number, title, author, timeout, content_source, text, img)
    except Exception as err:
        mistake(url, err)


def gainBelowUrl(reponse):
    # 获取下一篇新闻的URL
    html = etree.HTML(reponse.text)
    next_chepter = html.xpath('//*[@id="layer8A0AB3AA964FD517CD3E813B876C3806"]/div/div[5]/div/div[2]/a/@href')
    if not next_chepter:
        next_chepter = html.xpath('//div[@class="nextlist"]/a/@href')
    if next_chepter:
        return next_chepter[0]
    else:
        return "end"


def connent(number):
    # 连接网址，循环进行获取数据
    url = "http://www.haitunbc.com/page68.html?article_id=%s" % number
    while True:
        pattern = re.compile('\d+')
        number = re.findall(pattern, url)[1]
        if rechecking(number, come_from="haitunbc"):
            break
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            download(reponse, number, url)
            data = gainBelowUrl(reponse)
            if data == "end":
                break
            url = data
        else:
            err = reponse.status_code
            mistake(url, err)
            break


def getUrl(reponse):
    html = reponse.text
    pattern_url = re.compile("[a-zA-z]+://[^\s]*\.html\?article_id=\d+")
    urls = re.findall(pattern_url, html)
    num = []
    for url in urls:
        pattern_num = re.compile("\d+")
        number = re.findall(pattern_num, url)[1]
        num.append(int(number))
    number = max(num)
    return number


def starts():
    url = "http://www.haitunbc.com/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        number = getUrl(reponse)
        connent(number)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()
