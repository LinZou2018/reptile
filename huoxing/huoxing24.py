import requests
from lxml import etree
import re
from error_document import mistake
from headers import header
from mongodb_news import storageDatabase, rechecking


def storage(title, author, subhead, time, source, text, number):
    dicts = {
        "_id": number,
        "title": title,
        "subhead": subhead,
        "author": author,
        "release_time": time,
        "source": source,
        "main": text,
    }
    storageDatabase(dicts, come_from="huoxing24")


def download(html, url):
    try:
        # 获取编号
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)[1]
        # 判断数据库中是否已经下载过
        if rechecking(number, come_from="huoxing24"):
            return
        # 匹配发布时间
        pattern_time = re.compile('([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))')
        time = re.findall(pattern_time, html)[0]
        # print(time)
        # 匹配标题
        pattern_title = re.compile('<h1 style[\s\S]*?</h1>')
        titles = re.findall(pattern_title, html)[0]
        title = titles.split()[-2]
        # print(title)
        # 匹配副标题
        pattern_subhead = re.compile('<h2>[\s\S]*?</h2>')
        fu_title = re.findall(pattern_subhead, html)[0]
        subhead = fu_title[4: -5]
        # print(fu_title)
        # 匹配文本的来源
        pattern_source = re.compile('本文来源： <span>[\s\S]*?</span>')
        sources = re.findall(pattern_source, html)[0]
        pattern = re.compile('>[\s\S]*?<')
        source = re.findall(pattern, sources)[0][1: -1] + "--" + url
        # print(source)
        # 匹配作者
        pattern_authors = re.compile('<p class="author">[\s\S]*?</p>')
        authors = re.findall(pattern_authors, html)[0]
        pattern_author = re.compile('[\u4e00-\u9fa5]+')
        author = re.findall(pattern_author, authors)[0]
        # print(author)
        # 匹配新闻信息
        down_page = etree.HTML(html)
        texts = down_page.xpath('//div[@class=""]')[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        # print(text)
        # 进行存储信息
        storage(title, author, subhead, time, source, text, number)
    except Exception as err:
        mistake(url, err)


def starts():
    # 从主页查找新闻信息
    url = "http://www.huoxing24.com/"
    reponse = requests.get(url, headers=header())
    reponse.encoding = "utf-8"
    html = reponse.text
    pattern = re.compile('<div class="index-news-list">[\s\S]*?<div class="shadow">')
    texts = re.findall(pattern, html)
    # print(texts)
    n = 1
    for text in texts:
        # print(n)
        n += 1
        # 进行遍历，加载新闻网址
        pattern = re.compile('[a-zA-z]+://[^\s]*\.html')
        url = re.findall(pattern, text)[0]
        reponse = requests.get(url, headers=header())
        reponse.encoding = "utf-8"
        # 判断网址能否加载
        if reponse.status_code == 200:
            html = reponse.text
            download(html, url)
        else:
            err = "reponse.status_code为:" + reponse.status_code
            mistake(url, err)

if __name__ == "__main__":
    starts()
