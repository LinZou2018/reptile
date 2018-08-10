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
    storageDatabase(dicts, come_from="shilian")


def next_page(url, html):
    try:
        url_num = html.xpath('/html/body/div[2]/div[1]/div/div[4]/ul/li[5]/a/@href')[0]
        pattern = re.compile('\d+_\d')
        re_string = re.findall(pattern, url_num)[0]
        pattern_url = re.compile('\d+')
        url = re.sub(pattern_url, re_string, url)
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "gbk"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            texts = html.xpath('/html/body/div[2]/div[1]/div/div[3]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            return text
        else:
            err = reponse.status_code
            mistake(url, err)
    except Exception as err:
        mistake(url, err)


def download(url, number):
    print("shilian")
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "gbk"
    if reponse.status_code == 200:
        try:
            html = etree.HTML(reponse.text)
            # 获取标题、文章内容、作者和来源
            title = html.xpath('/html/body/div[2]/div[1]/div/h1/text()')[0]
            theSidebar = html.xpath('/html/body/div[2]/div[1]/div/div[1]/text()')
            author = "世链财经：" + theSidebar[0]
            timeout = theSidebar[1]
            classify = html.xpath('/html/body/div[2]/div[1]/div/div[1]/a/text()')
            source = ("世链财经--%s：" % classify) + url
            texts = html.xpath('/html/body/div[2]/div[1]/div/div[3]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            pattern = re.compile("下一页")
            exist = re.findall(pattern, reponse.text)
            if len(exist):
                next_text = next_page(url, html)
                text = text + next_text
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
        num = re.findall(pattern_num, url)
        number = ""
        for i in num:
            number += i
        if rechecking(number, come_from="shilian"):
            break
        download(url, number)


def starts():
    urls = ["http://shilian.com/zixun/redian/list_7_%s.html", "http://shilian.com/zixun/caijing/list_5_%s.html",
            "http://shilian.com/zixun/zhuanlan/list_21_%s.html", "http://shilian.com/zixun/hangye/list_22_%s.html",
            "http://shilian.com/xiangmu/list_17_%s.html", "http://shilian.com/huiyi/list_18_%s.html",
            "http://shilian.com/jishu/list_15_%s.html", "http://shilian.com/baike/list_19_%s.html"]
    for urlOne in urls:
        n = 1
        while True:
            url = urlOne % n
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