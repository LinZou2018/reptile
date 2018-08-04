import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(title, authors, times, source, main, number, subtitle):
    # 存入数据库
    time = ""
    author = ""
    for i in times:
        time += i
    for i in authors:
        author += i + " "
    dicts = {
        "_id": number,
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "release_time": time,
        "source": source,
        "main": main,
    }
    # 存入文档
    storageDatabase(dicts, come_from="fn")


def download(url, html):
    try:
        # 筛选数据
        # 新闻的编号
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)[0]
        # 判断数据库中是否已经下载过
        if rechecking(number, come_from="fn"):
            return
        # 发布时间
        pattern_time = re.compile('([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))')
        times = re.findall(pattern_time, html)[0][0: 2]
        html = etree.HTML(html)
        # 新闻标题
        texts = html.xpath('//h1[@class="entry-title"]')[0]
        title = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()[0]
        # 新闻作者
        texts = html.xpath('//div[@class="entry-info"]')[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        num = text.index('•')
        authors = text[0: num]
        # 新闻导读"副标题"
        texts = html.xpath('//div[@class="entry-excerpt"]')[0]
        subtitle = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()[0]
        # 新闻正文
        texts = html.xpath('//div[@class="entry-content clearfix"]')[0]
        mains = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        main = mains[0: -1]
        # 新闻来源
        source = main[-1]
        # 进行存储
        storage(title, authors, times, source, main, number, subtitle)
    except Exception as err:
        mistake(url, err)

def read_content(urls):
    n = 1
    for url in urls:
        # 循环获取上一篇内容
        while True:
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                download(url, html)
                # 匹配上一篇新闻的url
                pattern = re.compile('<a href="[a-zA-z]+://www.fn.com[^\s]*\.html" t[\s\S]*?&laquo; 上一篇')
                texts = re.findall(pattern, html)[0]
                pattern = re.compile('[a-zA-z]+://www.fn.com[^\s]*\.html')
                url = re.findall(pattern, texts)[0]
            else:
                err = "reponse.status_code为:" + reponse.status_code
                mistake(url, err)
                # print("结束")
                break
            n += 1


def starts(headers):
    # 从首页开始查询网址
    url = "http://www.fn.com/"
    reponse = requests.get(url, headers=headers)
    reponse.encoding = "utf-8"
    html = reponse.text
    # 获取首页所有的新闻网址
    pattern = re.compile('[a-zA-z]+://www.fn.com/news/[^\s]*\.html')
    urls_news = re.findall(pattern, html)
    pattern = re.compile('[a-zA-z]+://www.fn.com/dapth/[^\s]*\.html')
    urls_dapth = re.findall(pattern, html)
    urls = list(set(urls_news + urls_dapth))
    # print(urls)
    read_content(urls)


if __name__ == "__main__":
    starts(headers.header())


