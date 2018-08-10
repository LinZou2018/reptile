import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def download(reponse):
    html = reponse.text
    print(html)


def starts():
    url = "https://www.xinbinews.com/cms/information.php?c=index"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        download(reponse)


if __name__ == '__main__':
    starts()