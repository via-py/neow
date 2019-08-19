# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  MongoHelper.py
@Description    :  mongodb操作集合
@CreateTime     :  2019/8/18 17:02
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
from pymongo import MongoClient
from conf.ConfigGetter import config


class MongoHelper(object):
    def __init__(self, name, host, port, **kwargs):
        self.name = name
        self.client = MongoClient(host, port, **kwargs)
        self.db = self.client[name]
        self.collection = self.db[config.table]

    def get(self, key, kwargs):
        value = kwargs[key]
        return self.collection.find_one({key: value})

    def put(self, key, doc):
        return self.collection.insert_one(doc)

    def update(self, key, value, kwargs):
        return self.collection.update_one({key: value}, {'$set': kwargs})

    def delete(self, key, kwargs):
        value = kwargs[key]
        return self.collection.delete_one({key: value})

    def exists(self, key, **kwargs):
        value = kwargs[key]
        result = self.collection.find({key: value})
        return True if len(result) else False

    def pop(self, **kwargs):
        return self.collection.find({'$pop': {'field': 1}})

    def getAll(self):
        return self.collection.find()

    def clear(self):
        self.collection.delete_many({})

    def changeTable(self, name):
        self.collection = self.db[name]

    def getNumber(self):
        return len(self.collection.find({}))


if __name__ == '__main__':
    db = MongoClient('proxy_pool', '127.0.0.1', 27017)

    # def update(self, criteria, objNew,):
    #     """
    #
    #     :param criteria: 查询条件
    #     :param objNew: update对象和一些更新操作符
    #     upsert：如果不存在update的记录，是否插入objNew这个新的文档，true为插入，默认为false，不插入。
    #     multi：默认是false，只更新找到的第一条记录。如果为true，把按条件查询出来的记录全部更新。
    #
    #     :return:
    #     """
    #     return self.db.update(criteria, objNew, upsert=True, multi=False)

