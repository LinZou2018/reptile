import requests
import re
from lxml import etree
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def download(url, number):
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        print(html)
        pattern = re.compile('<div class="hq_information_container">[\s\S]*?<!-- 底部广告 -->')
        texts = re.findall(pattern, html)
        print(texts)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile('/Content/[^\s]*?data=[^\s]*?2C')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    for i in urls:
        url = "https://ihuoqiu.com" + i
        pattern = re.compile('(/Content/[^\s]*?data=)([^\s]*?2C)')
        num = re.findall(pattern, url)[0]
        number = num[1]
        if rechecking(number, come_from="ihuoqiu"):
            continue
        download(url, number)
        break


def starts():
    urls = ["https://ihuoqiu.com/Home/Index", "https://ihuoqiu.com/Home/information",
            "https://ihuoqiu.com/Home/encyclopedias"]
    for url in urls:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            getUrl(reponse)
            break


if __name__ == '__main__':
    starts()