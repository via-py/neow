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

    def get(self, condition, many):
        """
        获取符合条件的数据
        :param condition: (dict)
        :param many: (bool)
        :return:dict
        """
        if many:
            return self.collection.find(condition)
        return self.collection.find_one(condition)

    def put(self, doc, many):
        """
        插入数据
        :param doc: (dict)
        :param many: (bool)
        :return:str
        """
        if many:
            return self.collection.insert_many(doc).inserted_ids
        return self.collection.insert_one(doc).inserted_id

    def update(self, condition, doc, many):
        """
        更新数据
        :param condition: (dict)
        :param doc: (dict)
        :param many: (bool)
        :return:int
        """
        if many:
            return self.collection.update_many(condition, {'$set': doc}).modified_count
        return self.collection.update_one(condition, {'$set': doc}).modified_count

    def delete(self, condition, many):
        """
        删除数据
        :param condition: (dict)
        :param many: (bool)
        :return:int
        """
        if many:
            return self.collection.delete_many(condition).deleted_count
        return self.collection.delete_one(condition).deleted_count

    def exists(self, condition):
        """
        判断是否存在
        :param condition:(dict)
        :return:bool
        """
        result = self.collection.find(condition)
        return True if len(result) else False

    def pop(self, **kwargs):
        """
        弹出最后一个数据
        :param kwargs:
        :return:dict
        """
        return self.collection.find({'$pop': {'field': 1}})

    def getAll(self):
        """
        获取所有数据
        :return:list
        """
        return self.collection.find()

    def clear(self):
        """
        清空数据集合
        :return:
        """
        self.collection.delete_many({})

    def changeTable(self, name):
        """
        切换数据集合
        :param name:
        :return:
        """
        self.collection = self.db[name]

    def getNumber(self):
        """
        获取数据个数
        :return:int
        """
        return self.collection.find({}).count()


if __name__ == '__main__':
    db = MongoHelper('proxy_pool', '127.0.0.1', 27017)

