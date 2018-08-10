import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, author, source, statement, text):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": text,
        "statement": statement,
    }
    storageDatabase(dicts, come_from="queding")


def next_page(url, html):
    try:
        # 有第二页就获取第二页的文章内容
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
    print("queding")
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "gbk"
    if reponse.status_code == 200:
        try:
            html = etree.HTML(reponse.text)
            # 获取标题、文章内容、作者和来源
            title = html.xpath('/html/body/div[2]/div[1]/div/h1/text()')[0]
            theSidebar = html.xpath('/html/body/div[2]/div[1]/div/div[1]/text()')
            author = theSidebar[0]
            timeout = theSidebar[1]
            classify = html.xpath('/html/body/div[2]/div[1]/div/div[1]/a/text()')
            source = ("确定财经--资讯--%s：" % classify) + url
            texts = html.xpath('/html/body/div[2]/div[1]/div/div[3]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            pattern = re.compile("下一页")
            exist = re.findall(pattern, reponse.text)
            if len(exist):
                next_text = next_page(url, html)
                text = text + next_text
            # # 新闻有声明的问题
            statements = html.xpath('/html/body/div[2]/div[1]/div/div[5]')[0]
            statement = etree.tostring(statements, method="text", encoding="utf8").decode("utf8").split()
            # 将获取的数据存入数据库
            storage(number, title, timeout, author, source, statement, text)
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
        url = "http://queding.cn" + i
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)[0]
        if rechecking(number, come_from="queding_alerts") or int(number) < 1000:
            break
        download(url, number)


def starts():
    urls = ["http://queding.cn/jishu/list_15_%s.html", "http://queding.cn/xueyuan/list_16_%s.html", "http://queding.cn/baike/list_19_%s.html"]
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