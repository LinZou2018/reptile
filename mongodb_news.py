import pymongo
import time

# 连接数据库
conn = pymongo.MongoClient('localhost', 27017)
db = conn['news']

# 打开对应数据库集合，存入数据
def deposit(dicts, come_form):
    cursor = db['%s' % come_form]
    storage_time = time.asctime(time.localtime(time.time()))
    dicts["storage_time"] = storage_time
    cursor.insert(dicts)


# 打开数据库的错误信息集合
def errorMessage(dicts, come_from):
    cursor = db['error']
    storage_time = time.asctime(time.localtime(time.time()))
    dicts["storage_time"] = storage_time
    dicts["the_error_source"] = "%s" % come_from
    cursor.insert(dicts)


def storageDatabase(dicts, come_from):
    # 判断是存入错误信息还是完整信息
    if come_from == "message":
        errorMessage(dicts, come_from)
    else:
        deposit(dicts, come_from)


def rechecking(number, come_from):
    # 查询对应数据库是否已经存在
    cursor = db['%s' % come_from]
    my_set = cursor.find({"_id": number})
    num = my_set.count()
    if num == 1:
        return True
    elif num == 0:
        return False

def max_id(come_from):
    # 查询编号最大值
    cursor = db['%s' % come_from]
    my_set = cursor.find().sort([("_id", -1)]).limit(1)
    number = 0
    for num in my_set:
        number = num["_id"]
    return number


def title_find(title, come_from):
    # 使用标题进行查询是否存入过
    cursor = db["%s" % come_from]
    my_set = cursor.find({"title": title})
    number = 0
    for num in my_set:
        number = num["title"]
    return number


def closeMongodb():
    conn.close()

