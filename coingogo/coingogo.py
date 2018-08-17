import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, original, translate, timeout, content_source, source, text, statement, img):
    dicts = {
        "_id": number,
        "title": title,
        "release_time": timeout,
        "author": author,
        "source": source,
        "content_source": content_source,
        "main": text,
        "statement": statement,
        "original": original,
        "translate": translate,
        "img": img,
    }
    storageDatabase(dicts, come_from="coingogo")


def download(reponse, number, url):
    try:
        print("coingogo")
        html = etree.HTML(reponse.text)
        # 获取标题
        title = html.xpath('/html/body/div/div[4]/div[1]/div[1]/text()')[0]
        # 获取发布时间
        timeout = html.xpath('/html/body/div/div[4]/div[1]/div[2]/span[1]/text()')[0]
        # 获取新闻的内容来源及声明
        ending = html.xpath('/html/body/div/div[4]/div[1]/div[6]')[0]
        statements = etree.tostring(ending, method="text", encoding="utf8").decode("utf8").split()
        # 判断新闻是否有内容来源信息或声明信息
        if len(statements) == 2:
            content_source = statements[0]
            statement = statements[1]
        else:
            content_source = "币源社区"
            statement = "版权声明：本文仅为传播消息之用，不代表币源社区立场，文章不构成投资建议。如需转载，请务必注明文章原作者以及来源，部分图片来源于网络，我们尊重版权，如有疑问敬请联系，我们将核实并删除。"
        # HTML标签可能不一样，可能是p或者div，获取对象
        texts = html.xpath('//*[@id="content"]/p')
        exist = html.xpath('//*[@id="content"]/div')
        # 判断是p还是div标记
        if len(texts) < len(exist):
            texts = exist
        else:
            # 有的文章会在div标签中出现文本
            branch = html.xpath('//*[@id="content"]/div/p')
            for i in branch:
                texts.append(i)
        main_text = []
        for i in texts:
            text = etree.tostring(i, method="text", encoding="utf8").decode("utf8")
            main_text.append(text)
        original = ""
        translate = ""
        author = "币源社区"
        text = main_text
        # 判断文本列表的长度，有的文本分段少，列表长度短
        if len(main_text) > 4:
            pattern = re.compile("原文")
            original = re.findall(pattern, main_text[-4])
            # 判断文章中是否出现有原文的网站
            if original:
                original = main_text[-4]
                author = main_text[-3]
                translate = main_text[-2]
                statement = statement + "文章" + main_text[-1]
                text = main_text[:-4]
        # 获取文章所用的图片
        img = html.xpath('//*[@id="content"]/img/@src')
        img.append(html.xpath('//*[@id="content"]/div/p/img/@src'))
        img.append(html.xpath('//*[@id="content"]/div/img/@src'))
        img.append(html.xpath('//*[@id="content"]/p/img/@src'))
        source = "币源社区"
        storage(number, title, author, original, translate, timeout, content_source, source, text, statement, img)
    except Exception as err:
        mistake(url, err)
        return True


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile('/news/\d+')
    urls = re.findall(pattern, html)
    urls = list(set(urls))
    for i in urls:
        url = "http://www.coingogo.com" + i
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        pattern = re.compile('\d+')
        # 获取信息的编号
        number = re.findall(pattern, url)[0]
        if rechecking(number, come_from="coingogo"):
            continue
        if reponse.status_code == 200:
            data = download(reponse, number, url)
            if data:
                continue
        else:
            err = reponse.status_code
            mistake(url, err)


def starts():
    urls = ["http://www.coingogo.com/news/default/index?parent=1", "http://www.coingogo.com/news/default/index?parent=6",
            "http://www.coingogo.com/news/default/index?parent=7", "http://www.coingogo.com/news/default/index?parent=8",
            "http://www.coingogo.com/news/default/index?parent=9", "http://www.coingogo.com/news/default/index?parent=10",
            "http://www.coingogo.com/news/default/index?parent=11", "http://www.coingogo.com/news/default/index?parent=43",]
    for url in urls:
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            getUrl(reponse)
        else:
            err = reponse.status_code
            mistake(url, err)


if __name__ == '__main__':
    starts()