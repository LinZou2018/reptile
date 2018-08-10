import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, source, label, text, statement, img):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "source": source,
        "main": text,
        "main_img": img,
        "statement": statement,
        "label": label,
    }
    storageDatabase(dicts, come_from="btc123")


def download(reponse, url, number):
    try:
        print("btc123")
        html = etree.HTML(reponse.text)
        # 获取信息的标题
        title = html.xpath('//*[@id="newsDetails-box"]/div/div[1]/div/p/text()')[0]
        # 获取文章来源以及正则匹配其来源网址
        source = html.xpath('//*[@id="newsDetails-box"]/div/div[1]/div/div[1]/div[1]/text()')[1].split()[0]
        pattern = re.compile('稿源：[\s\S]*?\.com\/')
        source_url = re.findall(pattern, reponse.text)
        if source_url:
            source = source + "--" + source_url[0]
        # 对文章有分类，获取文章的标签
        label = html.xpath('//*[@id="newsDetails-box"]/div/div[1]/div/div[1]/div[2]/text()')[1].split()[0]
        # 注意author的正则表达式后面有一个空格，匹配数据的结尾
        pattern = re.compile('编译：[\s\S]*? ')
        author = re.findall(pattern, reponse.text)
        if author:
            author = author[0]
        else:
            author = "btc123 : " + url
        # 文章有声明
        statement = html.xpath('//*[@id="newsDetails-box"]/div/div[1]/div/div[5]/text()')[0].split()[0]
        # 获取正文
        texts = html.xpath('//*[@id="bind-content"]/@value')[0]
        texts = etree.HTML(texts)
        text = texts.xpath('//div')[0]
        text = etree.tostring(text, method="text", encoding="utf8").decode("utf8").split()
        # 正文中出现的图片
        img = texts.xpath('//div/p/img/@src')
        storage(number, title, author, source, label, text, statement, img)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile("news/[^\s]*\/\d+")
    urls = re.findall(pattern, html)
    url_number = []
    # 在网页中获取信息的最大编号
    for i in urls:
        pattern_num = re.compile("\d+")
        num = re.findall(pattern_num, i)
        url_number.append(num)
    max_number = int(max(url_number)[0])
    reload = 0
    while True:
        try:
            url = "https://www.btc123.com/news/newsDetails/%s" % max_number
            reponse_news = requests.get(url, headers=headers.header())
            reponse_news.encoding = "utf-8"
            # 判断在数据库中是否已经存入
            if rechecking(max_number, come_from="btc123"):
                break
            if reponse_news.status_code == 200:
                download(reponse_news, url, max_number)
                max_number -= 1
            else:
                err = reponse_news.status_code
                mistake(url, err)
                # 可以重新加载三次网页
                if reload == 3:
                    break
                reload += 1
        except:
            if reload == 3:
                break
            reload += 1


def starts():
    reload = 0
    url = "https://www.btc123.com/news"
    while True:
        try:
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            # 判断网页是否加载成功
            if reponse.status_code == 200:
                getUrl(reponse)
                # 加载成功也就结束循环
                break
            else:
                # 可以重新加载三次
                if reload == 3:
                    print("网络连接失败")
                    break
                reload += 1
        except:
            if reload == 3:
                break
            reload += 1


if __name__ == '__main__':
    starts()