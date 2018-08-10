import requests
from lxml import etree
import re
import headers
from error_document import mistake
from mongodb_news import storageDatabase, rechecking


def storage(number, title, timeout, main_texts, source):
    main = ""
    for main_text in main_texts:
        main += main_text + " "
    dicts = {
        "_id": number,
        "title": title,
        "author": "核财经快讯",
        "release_time": timeout,
        "source": source,
        "main": main,
    }
    storageDatabase(dicts, come_from="hecaijing_alerts")


def download(urls):
    for url_one in urls:
        try:
            print("hecaijing_alerts")
            url = "https://www.hecaijing.com" + url_one
            reponse = requests.get(url, headers=headers.header())
            reponse.encoding = "utf-8"
            html = etree.HTML(reponse.text)
            if reponse.status_code == 200:
                # 获取编号
                pattern_num = re.compile('\d+')
                number = re.findall(pattern_num, url)[0]
                # 判断数据库中是否已经下载过
                if rechecking(number, come_from="hecaijing_alerts"):
                    return
                times = html.xpath('/html/body/div[5]/div[1]/h2/text()')
                time_hour = html.xpath('/html/body/div[5]/div[1]/div/p[1]/span/text()')[0].split()
                timeout = times[1] + time_hour[0]
                title = html.xpath('/html/body/div[5]/div[1]/div/p[2]/text()')[0]
                main_texts = html.xpath('/html/body/div[5]/div[1]/div/div[1]/text()')[0].split()
                source = "核财经:" + url
                storage(number, title, timeout, main_texts, source)
            else:
                err = reponse.status_code
                mistake(url, err)
        except Exception as err:
            mistake(url_one, err)


def starts():
    url = 'https://www.hecaijing.com/kuaixun/'
    reponse = requests.get(url, headers=headers.header())
    reponse.encoding = "utf-8"
    html = reponse.text
    if reponse.status_code == 200:
        xmls = etree.HTML(html)
        urls = xmls.xpath('/html/body/div[5]/div[1]/ul/li/a/@href')
        # print(urls)
        download(urls)
    else:
        err = reponse.status_code
        mistake(url, err)

if __name__ == '__main__':
    starts()