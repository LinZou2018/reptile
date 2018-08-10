import requests
import re
import headers
from lxml import etree
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, author, source, text, statement, label):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": text,
        "statement": statement,
        "label": label,
    }
    storageDatabase(dicts, come_from="tuoluocaijing")


def download(reponse, url, number):
    try:
        print("tuoluocaijing")
        html = etree.HTML(reponse.text)
        # 获取标题
        title = html.xpath('/html/body/div[6]/div[1]/div/h1/text()')[0]
        # 获取发布时间
        timeout = html.xpath('/html/body/div[6]/div[1]/div/div[1]/span[3]/text()')[0]
        # 获取作者及作者的网址
        author_name = html.xpath('/html/body/div[6]/div[1]/div/div[1]/span[1]/a/text()')[0]
        author_ur = html.xpath('/html/body/div[6]/div[1]/div/div[1]/span[1]/a/@href')[0]
        author = author_name + "--https://www.tuoluocaijing.cn" + author_ur
        # 获取标签
        label = html.xpath('/html/body/div[6]/div[1]/div/div[3]/a/text()')
        # 获取正文
        texts = html.xpath("/html/body/div[6]/div[1]/div/div[2]")[0]
        text = etree.tostring(texts, method="text", encoding="utf8").decode("utf8").split()
        # 文章有声明
        statement = html.xpath('/html/body/div[6]/div[1]/div/p/text()')
        source = "陀螺财经--：https://www.tuoluocaijing.cn/"
        storage(number, title, timeout, author, source, text, statement, label)
    except Exception as err:
        mistake(url, err)


def getUrl(reponse):
    html = reponse.text
    pattern = re.compile("/article/detail-\d+\.html")
    urls = re.findall(pattern, html)
    url_number = []
    # 在网页中获取信息的最大编号
    for i in urls:
        pattern_num = re.compile("\d+")
        num = re.findall(pattern_num, i)
        url_number.append(num)
    max_number = int(max(url_number)[0])
    print(max_number)
    reload = 0
    while True:
        try:
            url = "https://www.tuoluocaijing.cn/article/detail-%s.html" % max_number
            reponse_news = requests.get(url, headers=headers.header())
            reponse_news.encoding = "utf-8"
            # 判断在数据库中是否已经存入
            if rechecking(max_number, come_from="btc123"):
                break
            if reponse_news.status_code == 200:
                download(reponse_news, url, max_number)
                max_number -= 1
            else:
                # 可以重新加载三次网页
                if reload == 3:
                    err = reponse_news.status_code
                    mistake(url, err)
                    break
                reload += 1
        except:
            if reload == 3:
                break
            reload += 1


def starts():
    reload = 0
    url = "https://www.tuoluocaijing.cn/"
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