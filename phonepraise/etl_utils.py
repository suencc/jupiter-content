# -*- coding:utf-8 -*-
import pymongo
import time
from bson import ObjectId

def is_export_new_result_coll():
    flag = input("please input(y/n), is export to new result collection:").strip()
    ret = False
    if flag == 'y': ret = True
    return ret    

def get_mongo_db():
    conn = pymongo.MongoClient('192.168.1.6',27017).phone
    conn.authenticate('phonedata','phonedata1805')
    return conn

# TODO 可以考虑输入collection的中间部分，得到 collection
def get_coll_result_proidlist(coll_name, appenddate=False):
    db = get_mongo_db()
    if appenddate:
        coll_name += time.strftime("_%Y%m%d", time.localtime())
    print('result coll:', coll_name)
    return db[coll_name]

# TODO 可以考虑输入collection的中间部分，得到 collection
def get_coll_result_comment(coll_name, appenddate=False):
    db = get_mongo_db()
    if appenddate:
        coll_name += time.strftime("_%Y%m%d", time.localtime())
    print('result coll:', coll_name)
    return db[coll_name]

# TODO 可以考虑输入collection的中间部分，得到 collection
# 目前只是输入collection名 得到 collection，实际作用较小，便于扩展增加此函数
def get_coll_crawl_proidlist(coll_name):
    db = get_mongo_db()
    return db[coll_name]

# TODO 可以考虑输入collection的中间部分，得到 collection
# 目前只是输入collection名 得到 collection，实际作用较小，便于扩展增加此函数
def get_coll_crawl_comment(coll_name):
    db = get_mongo_db()
    return db[coll_name]

# 把本次导出日志插入到 etl_export2result_log 集合
def set_coll_export2result_log(crawl_coll_name, minid, maxid):
    db = get_mongo_db()
    strtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    doc = {"crawl_coll_name": crawl_coll_name,
          "minid":minid,
          "maxid":maxid,
          "time":strtime}
    db.etl_export2result_log.insert_one(doc)    

# 根据要导出的集合名，查询etl_export2result_log，得到需要增量导出需要的“_id” 起始位置 
# TODO，当前实现只取插入时间最晚的一条记录，后续可以考虑综合多条记录来得到start_id
def get_start_id(crawl_coll_name):
    db = get_mongo_db()
    # maxid = ObjectId('591e9d15c24baefc6a915802')
    maxid = ObjectId('000000000000000000000000')
    
    rslt = db.etl_export2result_log.find({"crawl_coll_name": crawl_coll_name}).sort("_id", pymongo.DESCENDING)
    for rs in rslt:
        maxid = rs["maxid"]
        print('from log, maxid:', maxid)
        break
    print(crawl_coll_name, ' maxid:', maxid)
    return maxid

# 清空指定collection相关的log 和 结果
def clean_coll_exported_result(crawl_coll_name):
    db = get_mongo_db()
    if 'crawl' not in crawl_coll_name:
        print('clean_exported_result(), illegal collection name.')
        return False    
    del_coll_name = crawl_coll_name.replace('crawl', 'result')
    collectionlist = db.collection_names()
    for collection in collectionlist:
        if del_coll_name in collection: 
            ret = db.drop_collection(collection)
            print('drop %s status:' % collection, ret)
    db.etl_export2result_log.delete_many({'crawl_coll_name': crawl_coll_name})

'''
    下面是测试程序
'''
# if __name__ == "__main__":
#     set_coll_export2result_log("crawl_zol_proidlist", "5938ddaef006764a298604e0", "5938ddbef006764a298604f3")
#     set_coll_export2result_log("crawl_zol_proidlist", "5938ddaef006764a298604e0", "5938ddcef006764a298604f3")
#     get_start_id("crawl_zol_proidlist")    

#     cl = get_coll_crawl_proidlist("crawl_zol_proidlist")
#     print(cl)
#     cl = get_coll_result_proidlist("result_zol_proidlist", True)
#     print(cl)
#     cl = get_coll_result_proidlist("result_zol_proidlist", False)
#     print(cl)    
#     flag = is_export_new_result_coll()
#     print(flag)

#     clean_coll_exported_result('crawl_zol_proidlist')
#     startid = get_start_id('crawl_zol_proidlist')
#     col = get_coll_crawl_proidlist('crawl_zol_proidlist')
#     cursor = col.find({'_id': {'$gt': aa}})
#     for doc in cursor:
#         print(doc)

