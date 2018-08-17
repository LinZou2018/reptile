import requests
from lxml import etree
import headers
import re
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, source, text, classify, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": text,
        "classify": classify,
        "img": img,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="zhilianfm")


def download(number):
    try:
        url = 'http://www.zhilianfm.com/zlfmCms/kx/%s.jhtml' % number
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            classify = html.xpath('/html/body/section/legend/a[2]/text()')[0].split()[0]
            if classify == "快讯":
                return
            print("zhilianfm")
            # 获取标题
            title = html.xpath('/html/body/div[2]/section/h1/text()')[0]
            author_timeout_source = html.xpath('/html/body/div[2]/section/div[1]/text()')[0].split()
            # 获取作者
            author = author_timeout_source[1]
            # 获取发布时间
            timeout = author_timeout_source[0]
            # 获取信息来源
            source = author_timeout_source[2]
            # 获取文章内容
            texts = html.xpath('/html/body/div[2]/section/div[2]/p/text()')
            img = html.xpath('/html/body/div[2]/section/div[2]/p/img/@src')
            storage(number, title, author, timeout, source, texts, classify, img)
        else:
            err = reponse.status_code
            mistake(url, err)
            return True
    except Exception as err:
        mistake(url="http://www.zhilianfm.com/zlfmCms/", err=err)


def getUrl(reponse):
    html = reponse.text
    # 用正则匹配文章的网址及编号
    pattern_url = re.compile('[a-zA-z]+://[^\s]*\d+\.jhtml')
    urls = re.findall(pattern_url, html)
    url_number = []
    # 循环获取
    for url in urls:
        pattern_num = re.compile('\d+')
        num = re.findall(pattern_num, url)[0]
        url_number.append(int(num))
    # 得到最大编号
    number = max(url_number)
    return number


def starts():
    url = "http://www.zhilianfm.com/zlfmCms/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        # 获取文章的编号
        number = getUrl(reponse)
        while True:
            if rechecking(number, come_from="zhilianfm"):
                break
            data = download(number)
            if data:
                break
            number -= 1
    # else:
    #     err = reponse.status_code
    #     mistake(url, err)



if __name__ == '__main__':
    starts()