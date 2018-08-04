from mongodb_news import storageDatabase


def mistake(url, err):
    error = {
        "错误网页": url,
        "错误原因": str(err),
    }
    storageDatabase(error, come_from="message")
