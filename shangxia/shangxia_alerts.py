import requests
from lxml import etree
import headers
import time
from error_document import mistake
from mongodb_news import storageDatabase, max_id


def storage(number, title, author, timeout, source, text, statement, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout[0] + " " + timeout[1],
        "source": source,
        "main": text,
        "statement": statement,
        "img": img,
    }
    storageDatabase(dicts, come_from="shangxia_alerts")


def download(reponse, number, url):
    try:
        print("shangxia_alerts")
        html = etree.HTML(reponse.text)
        # 获取标题
        title = html.xpath('//*[@id="title"]/text()')[0]
        if not title:
            return True
        # 获取作者
        author = html.xpath('//div[@class="title_trade2"]/a/text()')[0]
        # 获取发布时间
        timeout = html.xpath('//div[@class="title_trade2"]/text()')[0].split()[1:3]
        # 获取信息来源
        source = html.xpath('/html/body/div[11]/div[6]/text()')[1].split()[0]
        # 文章的声明
        statement_object = html.xpath('/html/body/div[11]/div[7]')[0]
        statement_list = etree.tostring(statement_object, method="text", encoding="utf8").decode("utf8").split()
        statement = ""
        for i in statement_list:
            statement += i + " "
        # 获取文章内容
        texts = html.xpath('//*[@id="content"]')[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        # 获取信息使用的图片
        img_img = html.xpath('//*[@id="content"]/img/@src')
        img_div = html.xpath('//*[@id="content"]/div/img/@src')
        img_p = html.xpath('//*[@id="content"]/p/img/@src')
        img = img_img + img_div + img_p
        storage(number, title, author, timeout, source, text, statement, img)
    except Exception as err:
        mistake(url, err)


def starts():
    n = 2016
    tf = True
    # 判断数据库是否已经存在内容
    number = max_id(come_from="shangxia_alerts")
    if number:
        n = number + 1
        tf = False
    while True:
        try:
            url = "https://www.shangxia.net/kuaixun/1/%s.html" % n
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            if reponse.status_code == 200:
                data = download(reponse, n, url)
                if data:
                    break
            else:
                err = reponse.status_code
                mistake(url, err)
                break
            # 主要是运行的第一次
            if tf:
                n -= 1
            else:
                n += 1
        except TimeoutError:
            time.sleep(10)


if __name__ == '__main__':
    starts()