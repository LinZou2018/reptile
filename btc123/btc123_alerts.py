import requests
import re
import json
import time
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(findOne, release_time):
    dicts = findOne
    dicts["createText"] = release_time
    storageDatabase(dicts, come_from="btc123_alerts")


def UTCTime(timeout):
    # 判断时间是多久之前的
    pattern = re.compile("天")
    day = re.findall(pattern, timeout)
    pattern = re.compile("时")
    hour = re.findall(pattern, timeout)
    pattern = re.compile("分")
    minute = re.findall(pattern, timeout)
    pattern = re.compile("刚")
    nows = re.findall(pattern, timeout)
    pattern = re.compile("\d+")
    num = re.findall(pattern, timeout)[0]
    # 获取当前时间
    nowTheTime = int(time.time())
    # 计算新闻的发布的时间
    if len(day):
        marjin = int(num) * 24 * 60 * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(hour):
        marjin = int(num) * 60 * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(minute):
        marjin = int(num) * 60
        releaseTime = nowTheTime - marjin
        return time.asctime(time.localtime(releaseTime))
    elif len(nows):
        return time.asctime(time.localtime(time.time()))
    else:
        # 如果是精确的时间就返回此时间
        return timeout



def download(reponse, url):
    try:
        print("btc123_alerts")
        html = reponse.text
        # 将文档的json转换为字典
        text= json.loads(html)
        data = text["data"]
        for findOne in data:
            number = findOne["id"]
            if rechecking(number, "btc123_alerts"):
                break
            # 获取更精确的时间
            timeout = findOne["createText"]
            release_time = UTCTime(timeout)
            storage(findOne, release_time)
    except Exception as err:
        mistake(url, err)

def starts():
    n = 1
    s = 0
    while True:
        url = "https://apibtc.btc123.com/v1/index/getFlashPage?pageSize=20&pageNumber=%s" % n
        try:
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            # 判断网页是否加载完成
            if reponse.status_code == 200:
                download(reponse, url)
                n += 1
            else:
                err = reponse.status_code
                mistake(url, err)
                # 网页有三次重新加载
                if s == 2:
                    break
                s += 1
        except:
            # 网页可以重新加载
            if s == 2:
                break
            s += 1

if __name__ == '__main__':
    starts()