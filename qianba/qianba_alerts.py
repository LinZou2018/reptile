from mongodb_news import storageDatabase


def storage(number, title, author, timeout, source, text, label, point):
    dicts = {
        "_id": number,
        "title": title,
        "author": author,
        "release_time": timeout,
        "source": source,
        "main": text,
        "label": label,
        "classify": point
    }
    # print(dicts)
    storageDatabase(dicts, come_from="qianba_alerts")