import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, source, mains):
    main = ""
    for i in mains:
        main += i + " "
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "mian": main,
    }
    storageDatabase(dicts, come_from="youjiatuanjian")


def download(html, number, url):
    try:
        # 获取标题
        title = html.xpath('//*[@id="article-wrap"]/div/div[1]/div[1]/text()')[0]
        # 获取信息来源
        source_name = html.xpath('//*[@id="article-wrap"]/div/div[1]/div[3]/p[1]/span/text()')[0]
        source_url = html.xpath('//*[@id="article-wrap"]/div/div[2]/div[1]/div[1]/a/@href')[0]
        source = source_name + "--http://youjiatuanjian.com" + source_url
        # 获取发布时间
        timeout = html.xpath('//*[@id="article-wrap"]/div/div[1]/div[2]/div[2]/span/text()')[0]
        # 获取文章作者
        author = html.xpath('//*[@id="article-wrap"]/div/div[1]/div[2]/div[1]/span/text()')[0]
        # 获取信息内容
        texts = html.xpath('//*[@id="article-wrap"]/div/div[1]/div[3]')[0]
        main_text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        mains = main_text[1:]
        storage(number, title, author, timeout, source, mains)
    except Exception as err:
        mistake(url, err)


def getUrl(news):
    for new in news:
        url = "http://youjiatuanjian.com" + new
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        html = etree.HTML(reponse.text)
        if reponse.status_code ==200:
            # 获取编号
            pattern_num = re.compile('\d+')
            number = re.findall(pattern_num, url)[0]
            # 判断数据库中是否已经下载过
            if rechecking(number, come_from="youjiatuanjian"):
                return
            download(html, number, url)
        else:
            err = reponse.status_code
            mistake(url, err)


def starts():
    url = "http://youjiatuanjian.com/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    html = etree.HTML(reponse.text)
    news = html.xpath('//*[@id="view"]/li/a/@href')
    getUrl(news)


if __name__ == '__main__':
    starts()