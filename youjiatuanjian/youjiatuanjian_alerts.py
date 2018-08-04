import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(title, author, time, source, mains, number):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": time,
        "source": source,
        "mian": mains,
    }
    storageDatabase(dicts, come_from="youjiatuanjian_alerts")


def downloadOneMessage(text, time, url, number):
    try:
        # 精确时间
        mains = etree.tostring(text, method="text", encoding="utf8").decode("utf8").split()
        time = time + "--" + mains[0]
        # 将文本用空格连接，开始是被用空格隔开
        main_text = mains[2:]
        mains = ""
        for i in main_text:
            mains += i + " "
        # 从中获取信息的标题
        pattern = re.compile('【[\s\S]*?】')
        title = re.findall(pattern, mains)
        author = "布洛克财经-快讯"
        source = "布洛克财经-快讯:" + url
        storage(title, author, time, source, mains, number)
    except Exception as err:
        mistake(url, err)


def download(url, html):
    try:
        # 匹配快讯发布时间
        time = html.xpath('//*[@id="kuaixun-wrap"]/div/div[1]/div[1]/text()')[0]
        texts = html.xpath('//*[@id="view"]/li')
        n = 1
        for text in texts:
            # 获取没条快讯的唯一编号
            num = html.xpath('//*[@id="view"]/li[%s]/a/div[1]/div[2]/@onclick' % n)
            pattern = re.compile('\d+')
            number = re.findall(pattern, num[0])[0]
            # 判断数据库中是否已经下载过
            if rechecking(number, come_from="youjiatuanjian_alerts"):
                return
            downloadOneMessage(text, time, url, number)
            n += 1
    except Exception as err:
        mistake(url, err)


def starts():
    # 布洛克财经快讯新闻没有详情信息页
    url = "http://youjiatuanjian.com/newsflash/index.html"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    # 判断网页是否加载
    if reponse.status_code == 200:
        html = etree.HTML(reponse.text)
        download(url, html)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()