import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, title_find


def storage(title, timeout, main):
    dicts = {
        "title": title,
        "release_time": timeout,
        "author": "币报道--币快讯",
        "source": "币报道",
        "main": main,
    }
    storageDatabase(dicts, come_from="bibaodao_alerts")


def download(reponse, url):
    try:
        print("bibaodao_alerts")
        html = etree.HTML(reponse.text)
        texts = html.xpath('/html/body/div/div[3]/div[2]/div/div/div/div[1]/div[2]/div')
        for text in texts:
            data = etree.tostring(text, method="text", encoding="utf8").decode("utf8").split()
            timeout = data[0] + " " + data[1]
            mains = data[2:]
            main = ""
            for i in mains:
                main += i + " "
            pattern = re.compile("【[\s\S]*?】")
            title = re.findall(pattern, main)[0]
            if title_find(title, come_from="bibaodao_alerts"):
                return True
            storage(title, timeout, main)
    except Exception as err:
        mistake(url, err)


def starts():
    n = 1
    while True:
        url = 'https://www.bibaodao.com/newsflash/p/%s.html' % n
        reponse = requests.get(url, headers=headers.header(), verify=False)
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            data = download(reponse, url)
            if data:
                break
        else:
            err = reponse.status_code
            mistake(url, err)


if __name__ == '__main__':
    starts()