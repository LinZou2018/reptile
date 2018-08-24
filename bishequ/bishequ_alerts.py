import json
import time
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "Hm_lvt_554c268f4979cd8ffd030cc4507df8c4=1534475117; JSESSIONID=740F887EE08A0DDF0A2C713EBD6F432E; Hm_lpvt_554c268f4979cd8ffd030cc4507df8c4=1534484238",
    "Host": "bishequ.com",
    "Origin": "http://bishequ.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://bishequ.com/exchangelist",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


def storage(text, content, timeout):
    dicts = {
        "_id": text["id"],
        "title": text["title"],
        "author": "币社区--快讯",
        "release_tiem": timeout,
        "source": "币社区",
        "main": content,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="bishequ_alerts")


def download(reponse):
    print("bishequ_alerts")
    html = reponse.text
    texts = json.loads(html)
    data = texts["newsList"]
    for text in data:
        number = text["id"]
        if rechecking(number, come_from="bishequ_alerts"):
            return True
        content_text = etree.HTML(text["content"])
        content = content_text.xpath('//p/text()')
        if not content:
            content = content_text.xpath('//p/span/text()')
        timeout = time.asctime(time.localtime(int(text["createTime"])/1000))
        storage(text, content, timeout)


def starts():
    n = 0
    while True:
        data = {
            "sky": str(n),
        }
        url = 'http://bishequ.com/news/skynewsList'
        reponse = requests.post(url,data=data, headers=headers)
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


if __name__ == '__main__':
    starts()