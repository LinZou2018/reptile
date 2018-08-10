import requests
import json
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def download(reponse):
    html = reponse.text
    texts = json.loads(html)
    data = texts["data"]
    print(data)
    for text in data:
        number = text["currency_id"]
        print(text)
        break


def starts():
    url = "http://fengniaocaijing.com/api/route/article/detail?"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        download(reponse)


if __name__ == '__main__':
    starts()