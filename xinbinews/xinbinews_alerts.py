import requests
import re
# import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json,text/plain",
    "Host": "www.xinbinews.com",
    "Origin": "https://www.xinbinews.com",
    "Referer": "https://www.xinbinews.com/infomations.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
}


def download(reponse):
    html = reponse.text
    print(html)


def starts():
    url = "https://www.xinbinews.com/cms/information.php?c=index"
    reponse = requests.post(url, headers=headers)
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        download(reponse)


if __name__ == '__main__':
    starts()