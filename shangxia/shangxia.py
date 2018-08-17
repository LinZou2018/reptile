import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, source, main_text, takeaway, statement):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": main_text,
        "statement": statement,
        "takeaway": takeaway,
    }
    storageDatabase(dicts, come_from="shangxia")


def download(url, timeout, number):
    try:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            # 获取标题
            title = html.xpath('//*[@id="title"]/text()')[0]
            # 获取内容的来源
            timeout_source = html.xpath('/html/body/div[10]/div[1]/div[1]/text()')[0].split()
            sources = timeout_source[1: -1]
            source = ""
            for i in sources:
                source += i + " "
            # 内容的作者
            author = html.xpath('/html/body/div[10]/div[1]/div[5]/a/text()')[0]
            # 信息内容
            texts = html.xpath('//*[@id="content"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            main_text = ""
            for i in text:
                main_text += i + " "
            # 导读
            takeaway = html.xpath('/html/body/div[10]/div[1]/div[2]/text()')[0]
            # 文章的声明
            statement = html.xpath('/html/body/div[10]/div[1]/div[6]/text()')[0]
            storage(number, title, author, timeout, source, main_text, takeaway, statement)
        else:
            err = reponse.status_code
            mistake(url, err)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse, n):
    print("shangxia")
    # 上限设置
    reload = 1
    html = reponse.text
    # 匹配符合需求的内容
    pattern = re.compile('<div class="list" id="item[\s\S]*?<td width="10"> </td>[\s\S]*?<td width="10"> </td>')
    texts = re.findall(pattern, html)
    for text in texts:
        # 匹配其中的网址
        pattern_url = re.compile('[a-zA-z]+://[^\s]*\d+/\d+\.html')
        url = re.findall(pattern_url, text)[0]
        # 匹配编号和发布时间
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)
        number = str(n) + number[0] + number[1]
        if rechecking(number, come_from="shangxia"):
            reload += 1
            if reload > 4:
                return True
            continue
        pattern_time = re.compile('\[[\s\S]*?\]')
        timeout = re.findall(pattern_time, text)
        download(url, timeout, number)


def starts():
    # 获取翻页
    n = 1
    while True:
        url = "https://www.shangxia.net/news/index-htm-page-%s.html" % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            data = getUrl(reponse, n)
            n += 1
            if data:
                break
        else:
            err = reponse.status_code
            mistake(url, err)
            break


if __name__ == '__main__':
    starts()