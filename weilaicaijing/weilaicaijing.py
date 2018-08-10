import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, text, img, label, statement):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout[0] + " " + timeout[1],
        "source": "未来财经：http://weilaicaijing.com",
        "main": text,
        "picture": img,
        "label": label,
        "statement": statement,
    }
    storageDatabase(dicts, come_from="weilaicaijing")


def download(url, number):
    try:
        print("weilaicaijing")
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            html = etree.HTML(reponse.text)
            # 获取标题
            title = html.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[1]/h1/text()')[0]
            # 获取作者
            author = html.xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[1]/div[1]/div/span/text()')[0]
            # 获发布取时间
            timeout = html.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/text()')[0].split()
            # 获取文章内容
            texts = html.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[1]/div[3]/p')
            text = []
            for i in texts:
                textOne = etree.tostring(i, method="text", encoding="utf8").decode("utf8")
                text.append(textOne)
            # 获取所运用到的图片
            img = html.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[1]/div[3]/p/img/@src')
            # 文章的标签
            labels = html.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[1]/ul')[0]
            label = etree.tostring(labels, method="text", encoding="utf8").decode("utf8").split()
            # 文章的声明
            statement = html.xpath('//*[@id="app"]/div[2]/div[3]/div[1]/div[1]/div[4]/div[3]/text()')
            storage(number, title, author, timeout, text, img, label, statement)
        else:
            err = reponse.status_code
            mistake(url, err)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile("/article/\d+")
    urls = re.findall(pattern, html)
    for url in urls:
        url = "http://weilaicaijing.com" + url
        pattern = re.compile('\d+')
        number = re.findall(pattern, url)[0]
        if rechecking(number, come_from="weilaicaijing"):
            continue
        download(url, number)


def starts():
    reload = 0
    urls = ["http://weilaicaijing.com/", "http://weilaicaijing.com/IC",
            "http://weilaicaijing.com/interview", "http://weilaicaijing.com/dialogue",
            "http://weilaicaijing.com/evaluation"]
    for url in urls:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        while True:
            if reponse.status_code == 200:
                getUrl(reponse)
                break
            else:
                if reload == 3:
                    err = reponse.status_code
                    mistake(url, err)
                    break
                reload += 1


if __name__ == '__main__':
    starts()