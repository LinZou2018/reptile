import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, author, time, source, text):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": time,
        "source": source,
        "mian": text,
    }
    storageDatabase(dicts, come_from="hecaijing")


def download(reponse_branch, url, branch):
    try:
        # 获取编号
        pattern = re.compile('\d+')
        number = re.findall(pattern, url)[0]
        # 判断数据库中是否已经下载过
        if rechecking(number, come_from="hecaijing"):
            return
        html = etree.HTML(reponse_branch.text)
        # 获取标题、时间、作者、来源、内容
        title = html.xpath('/html/body/div[5]/div[1]/h1/text()')[0]
        author_compile = html.xpath('/html/body/div[5]/div[1]/p[2]/span[1]/text()')[0]
        author_name = html.xpath('/html/body/div[5]/div[1]/p[2]/span[2]/text()')[0].split()[0]
        author = author_compile+author_name
        times = html.xpath('/html/body/div[5]/div[1]/p[1]/text()')[0].split()
        time = times[1]
        source = ("核财经-%s:" % branch) + url + "--" + times[0]
        main_text = html.xpath('/html/body/div[5]/div[1]/div[3]')[0]
        text = etree.tostring(main_text, method="text", encoding="utf8").decode("utf8").split()
        storage(number, title, author, time, source, text)
    except Exception as err:
        mistake(url, err)


def checkUrl(reponse, branch):
    # 获取新闻url
    html = etree.HTML(reponse.text)
    urls = html.xpath('/html/body/div[5]/div[1]/ul/li/a/@href')
    for i in urls:
        url = "https://www.hecaijing.com" + i
        reponse_branch = requests.get(url, headers=headers.header())
        reponse_branch.encoding = "utf-8"
        if reponse_branch.status_code == 200:
            download(reponse_branch, url, branch)
        else:
            err = reponse_branch.status_code
            mistake(url, err)

def starts():
    # 新闻分为几类
    news = ["renwu", "shendu", "zhengce", "baike", "xinwen", "xinshou", "touyan"]
    for branch in news:
        # 获得每一页的url
        url = "https://www.hecaijing.com/%s/" % branch
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        if reponse.status_code == 200:
            checkUrl(reponse, branch)
        else:
            err = reponse.status_code
            mistake(url, err)


if __name__ == '__main__':
    starts()