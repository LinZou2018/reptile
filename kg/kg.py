import json
import re
import requests
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking



def download(reponse):
    html = reponse.text
    print(html)
    pattern_title = re.compile('(<h1>)([\s\S]*?)(</h1>)')
    title = re.findall(pattern_title, html)
    print(title)


def getUrl(html):
    html = etree.HTML(html)
    url_num = html.xpath('//*[@id="pane-金融"]/ul/li[1]/section/div[2]/p[1]/span/a/@href')
    print(url_num)
    pattern = re.compile('\d+')
    number = re.findall(pattern, url_num[0])
    if rechecking(number, come_from="kg"):
        return
    url = "https://www.kg.com/article/%s" % number
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        download(reponse)


def starts():
    url = "https://www.kg.com/jinrong"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        getUrl(html)


if __name__ == '__main__':
    starts()