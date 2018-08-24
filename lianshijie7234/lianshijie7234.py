import re
import json
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, content_source, data, statement, classify, img, label):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "content_source": content_source,
        "main": data,
        "classify": "本网站分类：" + classify,
        "statement": statement,
        "source": "链世界",
        "label": label,
        "img": img,
    }
    storageDatabase(dicts, come_from="lianshijie7234")


def download(html, number):
    print("lianshijie7234")
    # 获取标题，作者，发布时间
    title = html.xpath('/html/body/div[2]/div[1]/div[1]/h1/text()')[0]
    author = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/span[2]/text()')[0]
    timeout = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/span[3]/text()')[0]
    # 在本网站中的分类
    classify = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/span[1]/text()')[0]
    # 判断是原创还是转载
    content_source = html.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/a[2]/@href')
    if content_source:
        content_source = "来源地址：" + content_source[0]
    else:
        content_source = "链世界原创"
    # 获取文本，进行分割
    texts = html.xpath('/html/body/div[2]/div[1]/div[1]/div[2]')[0]
    text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
    if "|" in text:
        num = text.index("|")
        data = text[:num]
    else:
        data = text
    statement = "声明：链世界登载此文仅出于分享区块链知识，并不意味着赞同其观点或证实其描述。文章内容仅供参考，不构成投资建议。投资者据此操作，风险自担。此文如侵犯到您的合法权益，请联系我们100@7234.cn"
    # 获取本文使用的图片及标签
    img = html.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/p/img/@src')
    label = html.xpath('/html/body/div[3]/div[1]/div[1]/div[3]/ul/li/a/text()')
    storage(number, title, author, timeout, content_source, data, statement, classify, img, label)


def connect(url_data, number):
    # 连接网址进行下载数据
    url = "https://www.7234.cn" + url_data
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = etree.HTML(reponse.text)
        download(html, number)
    else:
        err = reponse.status_code
        mistake(url, err)
        return "end"


def getUrl(html):
    # 从中获取新闻的网址
    urls = html.xpath('//a/@href')
    for url in urls:
        # 进行判断是否是正确网址
        pattern = re.compile('(/[\s\S]*?/)(\d+)(#commentBox)')
        url_num = re.findall(pattern, url)
        if url_num:
            number = url_num[0][1]
            if rechecking(number, come_from="lianshijie7234"):
                return True
            url_data = url_num[0][0] + url_num[0][1]
            data = connect(url_data, number)
            if data == "end":
                return True


def starts():
    urls = ["https://www.7234.cn/fetch_articles/news", "https://www.7234.cn/fetch_articles/blockchain",
            "https://www.7234.cn/fetch_articles/tech", "https://www.7234.cn/fetch_articles/huodong",
            "https://www.7234.cn/fetch_articles/column"]
    for i in urls:
        n = 1
        while True:
            url = i + "?page=%s" % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                # 将json格式html文本转换为字典格式
                data = reponse.text
                data = json.loads(data)
                html = etree.HTML(data["html"])
                data = getUrl(html)
                if data:
                    break
                n += 1
            else:
                err = reponse.status_code
                mistake(url, err)
                break


if __name__ == '__main__':
    starts()