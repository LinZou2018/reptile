import requests
import re
import json
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(findOne, release_time, number, title):
    dicts = {
        "_id": number,
        "title": title,
        "author": "未来财经--快讯",
        "release_time": release_time,
        "source": findOne["source"],
        "main": findOne["text"],
        "url": findOne["url"],
    }
    storageDatabase(dicts, come_from="weilaicaijing_alerts")


def download(reponse, url):
    try:
        print("weilaicaijing_alerts")
        html = reponse.text
        # 将文档的json转换为字典
        text = json.loads(html)
        data = text["data"][0]
        timeout = data["time"]
        kuaixun_list = data["list"]
        for findOne in kuaixun_list:
            number = findOne["id"]
            if rechecking(number, "weilaicaijing_alerts"):
                return True
            time_hour = findOne["hour"]
            release_time = timeout + "  " + time_hour
            pattern = re.compile("【[\s\S]*?】")
            title = re.findall(pattern, findOne["text"])[0]
            storage(findOne, release_time, number, title)
    except Exception as err:
        mistake(url, err)

def starts():
    n = 1
    reload = 0
    while True:
        url = "http://weilaicaijing.com/api/Fastnews/lists?search_str=&page=%s" % n
        reponse = requests.get(url, headers=headers.header())
        reponse.encoding = "utf-8"
        # 判断网页是否加载完成
        if reponse.status_code == 200:
            already = download(reponse, url)
            if already:
                break
            n += 1
        # 此网站常出现503错误，重新加载5次
        elif reponse.status_code == 503:
            if reload == 5:
                err = reponse.status_code
                mistake(url, err)
                break
            reload += 1
        else:
            # 网页有三次重新加载
            if reload == 2:
                err = reponse.status_code
                mistake(url, err)
                break
            reload += 1

if __name__ == '__main__':
    starts()