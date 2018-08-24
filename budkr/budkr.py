import re
import headers
import requests
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, content_source, classify, text, statement, label, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "content_source": content_source,
        "classify": classify,
        "main": text,
        "source": "布道财经",
        "statement": statement,
        "label": label,
        "img": img,
    }
    storageDatabase(dicts, come_from="budkr")


def download(reponse, timeout, number):
    print("budkr")
    html = etree.HTML(reponse.text)
    # 获取标题、作者、分类
    title = html.xpath('/html/body/div[4]/div/div[1]/article/section[1]/header/h1/a/text()')
    author = html.xpath('//*[@id="article-latestArticles"]/div[1]/div[1]/span[1]/a/text()')
    classify = html.xpath('/html/body/div[4]/div/div[1]/article/section[1]/div/a/text()')
    # 获取文本分割，得到内容来源及声明
    texts = html.xpath('/html/body/div[4]/div/div[1]/article/section[2]')[0]
    data = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
    if "From：" in data:
        num = data.index("From：")
        content_source = data[num + 1]
        statement = data[num + 5:]
        text = data[:num]
    else:
        num = data.index("cambrian.render('tail')")
        content_source = '原创'
        statement = data[num + 1:]
        text = data[:num - 2]
    # 获取标签及使用的图片
    label = html.xpath('/html/body/div[4]/div/div[1]/article/section[3]/a/text()')
    img = html.xpath('/html/body/div[4]/div/div[1]/article/section[2]/p/img/@src')
    storage(number, title, author, timeout, content_source, classify, text, statement, label, img)


def getUrl(html):
    # 拆分获取数据
    pattern = re.compile('<div class="desc">[\s\S]*?</time>')
    texts = re.findall(pattern, html)
    for text in texts:
        # 得到URL以及发布时间
        pattern_url = re.compile('[a-zA-z]+://[^\s]*\.html')
        url = re.findall(pattern_url, text)[0]
        pattern_num = re.compile('\d+')
        number = int(re.findall(pattern_num, url)[0])
        if rechecking(number, come_from="budkr"):
            break
        pattern_time = re.compile('\d+-\d+-\d+ \d+:\d+')
        timeout = re.findall(pattern_time, text)[0]
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            download(reponse, timeout, number)
        else:
            err = reponse.status_code
            mistake(url, err)



def starts():
    urls = ["http://www.budkr.com/article?filter=1", "http://www.budkr.com/game?filter=1",
            "http://www.budkr.com/blockchain?filter=1", "http://www.budkr.com/ai?filter=1",
            "http://www.budkr.com/depth?filter=1", "http://www.budkr.com/research?filter=1",
            "http://www.budkr.com/capital?filter=1", "http://www.budkr.com/uinon?filter=1"]
    for url in urls:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = reponse.text
            getUrl(html)
        else:
            err = reponse.status_code
            mistake(url, err)


if __name__ == '__main__':
    starts()