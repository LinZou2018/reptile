import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, author, source, statement, text, label):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": text,
        "statement": statement,
        "label": label,
    }
    storageDatabase(dicts, come_from="shilian_alerts")


def download(url, number):
    print("shilian_alerts")
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "gbk"
    if reponse.status_code == 200:
        try:
            html = etree.HTML(reponse.text)
            # 获取标题、文章内容、作者和来源
            title = html.xpath('/html/body/div[2]/div[1]/div/h1/text()')[0]
            theSidebar = html.xpath('/html/body/div[2]/div[1]/div/div[1]/text()')
            author = "世链财经--快讯：" + theSidebar[0]
            timeout = theSidebar[1]
            # 信息的分类
            classify = html.xpath('/html/body/div[2]/div[1]/div/div[1]/a/text()')
            source = ("世链财经--资讯--%s：" % classify) + url
            texts = html.xpath('/html/body/div[2]/div[1]/div/div[3]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            # 新闻有声明的问题
            statements = html.xpath('/html/body/div[2]/div[1]/div/div[5]')[0]
            statement = etree.tostring(statements, method="text", encoding="utf8").decode("utf8").split()
            # 信息的标签
            label_head = html.xpath('/html/body/div[2]/div[1]/div/div[6]/div/text()')[0]
            label_word = html.xpath('/html/body/div[2]/div[1]/div/div[6]/div/a/text()')[0]
            label_url = html.xpath('/html/body/div[2]/div[1]/div/div[6]/div/a/@href')[0]
            label = label_head + label_word + "--http://www.shilian.com" + label_url
            # 将获取的数据存入数据库
            storage(number, title, timeout, author, source, statement, text, label)
        except Exception as err:
            mistake(url, err)
    else:
        err = reponse.status_code
        mistake(url, err)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile('/[^\s]*\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    for i in urls:
        url = "http://shilian.com" + i
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)[0]
        if rechecking(number, come_from="queding_alerts"):
            break
        download(url, number)


def starts():
    n = 1
    while True:
        url = "http://shilian.com/zixun/kuaixun/list_13_%s.html" % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            getUrl(reponse)
            n += 1
        else:
            err = reponse.status_code
            mistake(url, err)
            break

if __name__ == '__main__':
    starts()