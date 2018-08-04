import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, source, mains):
    main = ""
    for i in mains:
        main = i + " "
    dicts = {
        "_id": number,
        "title": title,
        "author": "FN-7x24h飞讯",
        "release_time": timeout,
        "source": source,
        "main": main,
    }
    storageDatabase(dicts, come_from="fn_alerts")


def download(html, time, n, text):
    try:
        # 获取编号
        source_url = html.xpath('//*[@id="wrap"]/div/div/div/div[2]/div[%s]/div[1]/h2/a/@href' % n)[0]
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, source_url)[0]
        # 判断数据库中是否已经下载过
        if rechecking(number, come_from="fn_alerts"):
            return
        # 获取文本
        main_text = etree.tostring(text, method="text", encoding="utf8").decode("utf8").split()
        n += 1
        # 获取标题、时间、来源、内容
        title = main_text[1]
        timeout = time + " " + main_text[0]
        mains = main_text[2: -8]
        source = "FN资讯：" + source_url
        storage(number, title, timeout, source, mains)
    except Exception as err:
        mistake(text, err)


def getUrl(url, html):
    try:
        html = etree.HTML(html)
        time = html.xpath('//*[@id="wrap"]/div/div/div/div[2]/div[1]/text()')[0]
        # print(time)
        texts = html.xpath('//div[@class="kx-item"]')
        # print(len(texts))
        n = 3
        for text in texts:
            download(html,time, n, text)
    except Exception as err:
        mistake(url, err)

def starts():
    # 从首页开始查询网址
    url = "http://www.fn.com/lives/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    html = reponse.text
    # 获取首页所有的新闻网址
    getUrl(url, html)

if __name__ == "__main__":
    starts()
