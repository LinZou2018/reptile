import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, timeout, text, label):
    dicts = {
        "_id": number,
        "title": title,
        "author": author + "--快讯",
        "release_time": timeout[0],
        "main": text,
        "source": "雷鹿财经：http://www.leilook.com",
        "label": label,
    }
    # print(dicts)
    storageDatabase(dicts, come_from="leilook_alerts")


def download(html, number, url):
    # 获取时间，以判断此网址是否是新闻信息网址，而不是存储图片的网址
    timeout = html.xpath('/html/body/section/div[1]/div/div/div[1]/div[2]/span[1]/text()')
    if not timeout:
        return True
    # 查看文章是否引用图片
    img_p = html.xpath('/html/body/section/div[1]/div/div/article/p/img/@src')
    img_div_p = html.xpath('/html/body/section/div[1]/div/div/article/div/p/img/@src')
    img = img_p + img_div_p
    if not img:
        try:
            # 没有引用图片则可能是快讯信息
            texts_div_p = html.xpath('/html/body/section/div[1]/div/div/article/div/p')
            texts_p = html.xpath('/html/body/section/div[1]/div/div/article/p')
            texts = texts_p + texts_div_p
            # 再次判断，以文章的内容作为依据判断是否是快讯信息
            if len(texts) > 2:
                pass
            else:
                # 获取标题
                title = html.xpath('/html/body/section/div[1]/div/div/h1/a/text()')
                print("leilook_alerts")
                # 本文的作者获取编辑
                author = html.xpath('/html/body/section/div[1]/div/div/div[1]/div[2]/a/text()')[0]
                # 文章标签
                label = html.xpath('/html/body/section/div[1]/div/div/div[1]/div[3]/span')[0]
                label = etree.tostring(label, method="text", encoding="utf8").decode("utf8").split()[0]
                text = []
                for i in texts:
                    textOne = etree.tostring(i, method="text", encoding="utf8").decode("utf8")
                    text.append(textOne)
                storage(number, title, author, timeout, text, label)
        except Exception as err:
            mistake(url, err)


def connent(number, reload):
    # 组合网址
    url = "http://www.leilook.com/archives/%s" % number
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        reload = 0
        html = etree.HTML(reponse.text)
        data = download(html, number, url)
        if data:
            return "pictrue"
    else:
        reload += 1
        if reload > 3:
            err = reponse.status_code
            mistake(url, err)
            return "over"


def getUrl(reponse):
    html = reponse.text
    # 用正则匹配文章的网址及编号
    pattern_url = re.compile('[a-zA-z]+://[^\s]*?archives/\d+')
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
    reload = 0
    url = "http://www.leilook.com/"
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    if reponse.status_code == 200:
        # 获取文章的编号
        number = getUrl(reponse)
        while True:
            if rechecking(number, come_from="leilook_alerts"):
                break
            data = connent(number, reload)
            if data == "pictrue":
                number -= 1
                continue
            elif data == "over":
                break
            number -= 1
    else:
        err = reponse.status_code
        mistake(url, err)


if __name__ == '__main__':
    starts()