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
    conn.close()


# 打开数据库的错误信息集合
def errorMessage(dicts, come_from):
    cursor = db['error']
    storage_time = time.asctime(time.localtime(time.time()))
    dicts["storage_time"] = storage_time
    dicts["the_error_source"] = "%s" % come_from
    cursor.insert(dicts)
    conn.close()


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
    conn.close()
    if num == 1:
        return True
    elif num == 0:
        return False

def jinse_id():
    # 查询编号最大值
    cursor = db['jinse_alerts']
    my_set = cursor.find({"_id": {"$gt": 43500}}).sort({"_id":-1}).limit(1)
    num = my_set[0]["_id"]
    conn.close()
    return num
