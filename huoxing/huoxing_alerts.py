import requests
from lxml import etree
import re
from error_document import mistake
from headers import header
from mongodb_news import storageDatabase, rechecking


def storage(title, time, source, main):
    dicts = {
        "title": title,
        "time": time,
        "author": "火星财经-快讯",
        "source": source,
        "main": main,
    }
    storageDatabase(dicts, come_from="huoxing_alerts")


def download(url):
    print("huoxing24_alerts")
    reponse = requests.get(url, headers = header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        try:
            # 获取编号
            pattern_num = re.compile('\d+')
            number = re.findall(pattern_num, url)[1]
            # 判断数据库中是否已经下载过
            if rechecking(number, come_from="huoxing_alerts"):
                return
            html = reponse.text
            down = etree.HTML(html)
            texts = down.xpath('/html/body/div[5]/div[1]')[0]
            text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
            # print(text)
            time = text[1] + text[0] + "日" + "--" + text[3] + "--" + text[4]
            # print(time)
            title = text[5]
            # print(title)
            mains = text[6: -4]
            main = ""
            for i in mains:
                main += i + " "
            # print(main)
            source = "火星财经快讯"
            storage(title, time, source, main)
        except Exception as err:
            mistake(url, err)
    else:
        err = "reponse.status_code为:" + reponse.status_code
        mistake(url, err)


def starts():
    url = 'http://www.huoxing24.com/livenews'
    reponse = requests.get(url, headers = header())
    reponse.encoding = "utf-8"
    html = reponse.text
    pattern = re.compile('[a-zA-z]+://[^\s]*\.html')
    down = re.findall(pattern, html)
    # print(down)
    n = 1
    for url in down:
        print(n)
        download(url)
        n += 1

if __name__ == "__main__":
    starts()