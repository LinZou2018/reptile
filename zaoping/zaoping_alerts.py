import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, title_find


def storage(title, date, text):
    dicts = {
        "title": title,
        "author": "早评财经--快讯",
        "release_time": date,
        "source": "早评财经",
        "main": text,
    }
    storageDatabase(dicts, come_from="zaoping_alerts")


def UTCTime(timeout):
    date = time.localtime()
    year = date.tm_year
    mon = date.tm_mon
    day = date.tm_mday
    date = str(year) + "-" + str(mon) + "-" + str(day) + "  " + timeout[0]
    return date


def download(reponse):
    html = reponse.text
    pattern = re.compile('<div class="control clear data-bottom-id">[\s\S]*?<!----></div>')
    texts = re.findall(pattern, html)
    for htmlObject in texts:
        html = etree.HTML(htmlObject + "</div>")
        titles = html.xpath('//div[@class="content"]/a[1]/text()')[0].split()
        title = ""
        for i in titles:
            title += i + " "
        if title_find(title, come_from="zaoping_alerts"):
            return True
        print("zaoping_alerts")
        data = html.xpath('//div[@class="content"]/a[2]/text()')[0].split()
        text = ""
        for i in data:
            text += i + " "
        timeout = html.xpath('//div[@class="time"]/text()')[0].split()
        if len(timeout) == 1:
            date = UTCTime(timeout)
        else:
            date = ""
            for i in timeout:
                date += i + "  "
        storage(title, date, text)


def starts():
    n = 1
    while True:
        url = "http://zaoping.net/list/6.html?page=%s&ids=6" % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            data = download(reponse)
            if data:
                break
            n += 1
        else:
            err = reponse.status_code
            mistake(url, err)
            break
    print("zaoping_alerts 结束")


if __name__ == '__main__':
    starts()