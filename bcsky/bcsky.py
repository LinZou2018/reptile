import re
import time
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, content_source, timeout, text, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "content_source": content_source,
        "main": text,
        "source": "链天下",
        "img": img,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="bcsky")


def download(html, number):
    print("bcsky")
    # 获取标题
    title = html.xpath('//*[@id="pic_main"]/h3/text()')[0]
    # 判断是否有作者
    author_source = html.xpath('//*[@id="pic_main"]/p/span[1]/text()')[0]
    pattern_author = re.compile('作者')
    author_exist = re.findall(pattern_author, author_source)
    if author_exist:
        author = author_source
        content_source = html.xpath('//*[@id="pic_main"]/p/span[2]/text()')[0]
        timeout = html.xpath('//*[@id="pic_main"]/p/span[3]/text()')[0]
    else:
        author = ""
        content_source = author_source
        timeout = html.xpath('//*[@id="pic_main"]/p/span[2]/text()')[0]
    texts = html.xpath('//*[@id="pic_main"]/div')[0]
    text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8")
    img = html.xpath('//*[@id="pic_main"]/div/p/img/@src')
    storage(number, title, author, content_source, timeout, text, img)


def connect(url, number):
    # 连接网址获取数据
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "urf-8"
    if reponse.status_code == 200:
        html = etree.HTML(reponse.text)
        download(html, number)
    else:
        err = reponse.status_code
        mistake(url, err)
        return True


def getURL(html, url):
    # 获取的数据没有顺序可言
    reload = 0
    # 获取详情网址
    pattern = re.compile('<ul>[\s\S]*?</ul>')
    texts = re.findall(pattern, html)[2]
    pattern_ex = re.compile('download')
    differentiate = re.findall(pattern_ex, url)
    if differentiate:
        pattern = re.compile('<ul class="ul_5" style="height: 1480px;">[\s\S]*?</ul>')
        texts = re.findall(pattern, html)[0]
    pattern_url = re.compile('/[^\s]*\.html')
    urls = re.findall(pattern_url, texts)
    urls = list(set(urls))
    for i in urls:
        url = "http://bcsky.pro" + i
        pattern_num = re.compile("\d+")
        number = re.findall(pattern_num, url)
        if len(number) == 4:
            number = number[3]
        else:
            number = number[0]
        if rechecking(number, come_from="bcsky"):
            if reload == 3:
                return True
            else:
                reload += 1
                continue
        data = connect(url, number)
        if data:
            return True


def starts():
    # 新闻的来源
    urls = ["http://bcsky.pro/news/china/index%s.html", "http://bcsky.pro/news/world/index%s.html",
            "http://bcsky.pro/download/index%s.html", "http://bcsky.pro/shop/index%s.html",
            "http://bcsky.pro/zhuantitougao/index%s.html", "http://bcsky.pro/baimeiliantan/index%s.html"]
    for i in urls:
        n = 1
        while True:
            # 翻页
            if n == 1:
                page = ""
            else:
                page = "_%s" % n
            try:
                url = i % page
                reponse = requests.get(url, headers=headers.header())
                reponse.encoding = "utf-8"
            except TimeoutError:
                time.sleep(10)
                continue
            if reponse.status_code == 200:
                html = reponse.text
                data = getURL(html, url)
                if data:
                    break
                n += 1
            else:
                err = reponse.status_code
                mistake(url, err)
                break


if __name__ == '__main__':
    starts()