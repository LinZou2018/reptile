import re
import headers
import requests
from error_document import mistake
from mongodb_news import storageDatabase, rechecking
from qianba import qianba_alerts


def storage(number, title, author, timeout, source, text, label, point):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": text,
        "label": label,
        "classify": point
    }
    # print(dicts)
    storageDatabase(dicts, come_from="qianba")


def classify(html, number, title, author, timeout, source, text, label):
    pattern_class = re.compile('(<li><a[\s\S]*?>)([\s\S]*?)(</a></li>)')
    point = re.findall(pattern_class, html)[0][1]
    if point == "快讯":
        print('qianba_alerts')
        qianba_alerts.storage(number, title, author, timeout, source, text, label, point)
    else:
        print("qianba")
        storage(number, title, author, timeout, source, text, label, point)


def download(html, number):
    pattern = re.compile('友情提示')
    distinguish = re.findall(pattern, html)
    if distinguish:
        return True
    pattern_title = re.compile('(<h2[\s\S]*?>)([\s\S]*?)(</h2>)')
    title = re.findall(pattern_title, html)[0][1]
    pattern_source = re.compile('(来源：<span><[\s\S]*?>)([\s\S]*?)(</a></span>)')
    source = re.findall(pattern_source, html)[0][1]
    pattern_time = re.compile('(<span>)(\d+-\d+-\d+ \d+:\d+:\d+)(</span>)')
    timeout = re.findall(pattern_time, html)[0][1]
    pattern_author = re.compile('(作者：<span>)([\s\S]*?)(</span>)')
    author = re.findall(pattern_author, html)
    # 可能有也可能没有
    if not author:
        author = ""
    else:
        author = author[0][1]
    pattern_text = re.compile('(<div class="d_txt">)([\s\S]*?)(</div>)')
    text = re.findall(pattern_text, html)[0][1]
    pattern_label = re.compile('(关键词：)([\s\S]*?)(</div>)')
    labelAll = re.findall(pattern_label, html)[0][1]
    pattern_ls = re.compile('(>)([\s\S]*?)(<)')
    labels = re.findall(pattern_ls, labelAll)
    label = []
    n = 0
    for i in labels:
        if n % 2 == 1:
            n += 1
            continue
        label.append(i[1])
        n += 1
    classify(html, number, title, author, timeout, source, text, label)


def connect(number):
    if rechecking(number, come_from="qianba"):
        return
    elif rechecking(number, come_from="qianba_alerts"):
        return
    else:
        while True:
            url = "http://qianba.com/%s.html" % number
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                html = reponse.text
                data = download(html, number)
                if data:
                    number -= 1
                    continue
                number -= 1
            else:
                err = reponse.status_code
                mistake(url, err)
                break


def getUrl(html):
    pattern = re.compile('[a-zA-z]+://[^\s]*\d+\.html')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    num = []
    for url in urls:
        pattern_num = re.compile('\d+')
        number = re.findall(pattern_num, url)
        num.append(int(number[0]))
    number = max(num)
    return number


def starts():
    url = "http://qianba.com/index.html"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = reponse.text
        number = getUrl(html)
        connect(number)
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()