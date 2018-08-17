import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, author, source, recommend, statement, texts):
    text = ""
    for i in texts:
        text += i + " "
    dicts = {
        "_id": number,
        "title": title,
        "author": author + "    --使用AD软件",
        "release_time": timeout,
        "source": source,
        "main": text,
        "recommend": recommend,
        "statement": statement,
    }
    storageDatabase(dicts, come_from="bitrating_alerts")


def download(url, number,timeout):
    print("bitrating_alerts")
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    # 判断网站是否加载成功
    if reponse.status_code == 200:
        try:
            html = etree.HTML(reponse.text)
            # 获取标题、文章内容、作者和来源
            title = html.xpath('/html/body/section/div[1]/div/header/div[1]/h1/a/text()')[0]
            texts = html.xpath('/html/body/section/div[1]/div/article/p/text()')
            author = html.xpath('/html/body/section/div[1]/div/article/div/text()')[0].split()[0]
            source = "比特评级--快讯：" + url
            # 新闻有推荐和声明的问题
            recommends = html.xpath('//div[@class="asb-post-footer"]')[0]
            recommend = etree.tostring(recommends, method="text", encoding="utf8").decode("utf")
            recommend += ": https://bitrating.com/wenda"
            statement = html.xpath('/html/body/section/div[1]/div/div[3]/text()')[0]
            # 将获取的数据存入数据库
            storage(number, title, timeout, author, source, recommend, statement, texts)
        except Exception as err:
            mistake(url, err)
    else:
        err = reponse.status_code
        mistake(url, err)


def getUrl(html):
    texts = html.xpath('//*[@id="home"]/article')
    for i in texts:
        # 为了获取精确的时间，还有快讯的详情
        timeout = i.xpath('time/@title')[0]
        url = i.xpath('div[2]/div[1]/div/a/@href')[0]
        pattern = re.compile('\d+')
        number = re.findall(pattern, url)[0]
        # 判断在数据库中是否已经下载过
        if rechecking(number, come_from="bitrating_alerts"):
            break
        download(url, number, timeout)


def starts():
    url = "https://bitrating.com/live"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    # 判断是否完成网页加载，或者是否有网
    if reponse.status_code == 200:
        pass
    else:
        err = reponse.status_code
        mistake(url, err)
        return
    html = etree.HTML(reponse.text)
    getUrl(html)


if __name__ == '__main__':
    starts()