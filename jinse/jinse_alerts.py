import requests
from lxml import etree
from error_document import mistake
from headers import header
from mongodb_news import storageDatabase, rechecking, jinse_id


def storage(titles, authors, times, url, mains):
    # 存入
    title = ""
    author = ""
    time = ""
    main = ""
    for i in titles:
        title += i
    authors[0] = "金色财经"
    for i in authors:
        author += i
    for i in times:
        time += i
    for i in mains:
        main += i
    dicts = {
        "title": title,
        "author": author,
        "time": time,
        "URL": url,
        "main": main,
    }
    storageDatabase(dicts, come_from="jinse_alerts")


def download(url):
    reponse = requests.get(url, headers = header())
    reponse.encoding = "utf-8"
    # 判断网页是否加载完成
    if reponse.status_code == 200:
        # 匹配时间正文再加以组合
        try:
            html = etree.HTML(reponse.text)
            texts = html.xpath('//*[@class="tc"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            times = text[0] + text[1]
            texts = html.xpath('//*[@class="time-detail"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            times = times + "--" + text[0]
            texts = html.xpath('//*[@class="intro-detail"]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            titles = text[0: 3]
            authors = text[-5:]
            mains = text[3: -5]
            storage(titles, authors, times, url, mains)
        except Exception as err:
            mistake(url, err)
        return  False
    else:
        err = "reponse.status_code为:" + reponse.status_code
        mistake(url, err)
        return True


def getUrl():
    number = jinse_id()
    if number:
        num = number
    else:
        num = 35000
        while True:
            # 判断数据库中是否已经下载过
            if rechecking(number=num, come_from="jinse_alerts"):
                break
            url = "https://www.jinse.com/lives/%s.htm" % num
            end = download(url)
            if end:
                break
            num -= 1
        num = 43500

    while True:
        num += 1
        # 判断数据库中是否已经下载过
        if rechecking(number=num, come_from="jinse"):
            return
        url = "https://www.jinse.com/lives/%s.htm" % num
        end = download(url)
        if end:
            break


def starts():
    url = "https://www.jinse.com/lives"
    reponse = requests.get(url, headers=header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        getUrl()
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == "__main__":
    starts()
