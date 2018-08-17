import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, content_source, statement, text):
    dicts = {
        "_id":number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "main": text,
        "source": "龙块：http://longkuai.com/",
        "content_source": content_source,
        "statement": statement,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="longkuai_alerts")


def download(html, number, url):
    # 查看文章是否引用图片
    img = html.xpath('//*[@id="main"]/div/div[1]/div[1]/p/img/@src')
    if not img:
        try:
            # 没有引用图片则可能是快讯信息
            text = html.xpath('//*[@id="main"]/div/div[1]/div[1]/p/text()')
            # 再次判断，以文章的内容作为依据判断是否是快讯信息
            if len(text) == 1 and text[0] == "\n":
                pass
            else:
                print("longkuai_alerts")
                # 获取标题
                title = html.xpath('//*[@id="main"]/div/div[1]/div[1]/h1/text()')[0]
                # 获取时间
                timeout = html.xpath('//*[@id="main"]/div/div[1]/div[1]/div[1]/span[1]/text()')[0]
                # 本文的作者获取编辑
                author = html.xpath('//*[@id="main"]/div/div[2]/div[1]/h1/text()')[0]
                # 内容的来源或者是原创
                content_source_object = html.xpath('//*[@id="main"]/div/div[1]/div[1]/div[2]')[0]
                content_source_text = etree.tostring(content_source_object, method="text", encoding="utf8").decode("utf8").split()
                content_source = ""
                for i in content_source_text:
                    content_source += i
                # 文章的声明
                statement = html.xpath('//*[@id="main"]/div/div[1]/div[1]/div[3]/text()')[0]
                storage(number, title, author, timeout, content_source, statement, text)
        except Exception as err:
            mistake(url, err)


def connent(number):
    # 155编号文章可能下架或者违规被封
    if number == 155:
        return
    # 组合网址
    url = "http://longkuai.com/article/id/%s" % number
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        html = etree.HTML(reponse.text)
        download(html, number, url)
    else:
        err = reponse.status_code
        mistake(url, err)
        return True


def getUrl(reponse):
    html = reponse.text
    # 用正则匹配文章的网址及编号
    pattern_url = re.compile('/article/id/\d+')
    urls = re.findall(pattern_url, html)
    url_number = []
    # 循环获取
    for url in urls:
        pattern_num = re.compile('\d+')
        num = re.findall(pattern_num, url)[0]
        url_number.append(int(num))
    # 得到最大编号
    number = max(url_number)
    return number


def starts():
    url = "http://longkuai.com/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        # 获取文章的编号
        number = getUrl(reponse)
        while True:
            # 独特排版
            if number == 146:
                number -= 1
                continue
            if rechecking(number, come_from="longkuai_alerts"):
                break
            data = connent(number)
            if data:
                break
            number -= 1
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()