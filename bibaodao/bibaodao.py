import requests
import re
# import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking

headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

def download(number, url):
    reponse = requests.get(url, headers=headers, verify=False)
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        pattern = re.compile('<div class="new_info_txt_box">[\s\S]*?</div>')
        texts = re.findall(pattern, html)
        print(texts)
        # pattern = re.compile('<div class="new_info_title">[\s\S]*?</div>')
        # texts = re.findall(pattern, reponse.text)[0]
        # print(texts)
        # pattern = re.compile('(>)([\s\S]*?)(<)')
        # lists = re.findall(pattern, texts)
        # title = lists[1][1]
        # print(title)
        # timeout = lists[5][1]
        # print(timeout)
        # html = etree.HTML(texts)
        # source = html.xpath('//div/p[2]/span/text()')[0].split()[0]
        # print(source)

def getUrl(reponse, url):
    url_news = url
    html = reponse.text
    # 进行筛选
    pattern = re.compile('/[a-z]*?/\d+\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    for i in urls:
        pattern = re.compile('\d+')
        number = re.findall(pattern, i)[0]
        if rechecking(number, come_from="bibaodao") or int(number) < 1000:
            break
        url = url_news + i
        download(number, url)
        break


def starts():
    # 新闻主要来自三个地址
    urls = ["https://www.bibaodao.com/industry/", "https://www.bibaodao.com/interpretation/",
            "https://www.bibaodao.com/technology/"]
    for url in urls:
        # 循环加载
        reponse = requests.get(url, headers=headers, verify=False)
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            getUrl(reponse, url)
            break


if __name__ == '__main__':
    starts()