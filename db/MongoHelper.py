# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  MongoHelper.py
@Description    :
@CreateTime     :  2019/8/18 17:02
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
from pymongo import MongoClient


class MongoHelper(object):
    def __init__(self, name, host, port, **kwargs):
        self.name = name
        self.client = MongoClient(host, port, **kwargs)
        self.db = self.client.proxy

    def find(self):
        """
        查询所有数据
        :return:
        """
        return self.db.find()

    def find_one(self, param):
        """
        查询符合条件的第一条数据
        :param param:
        :return:
        """
        return self.db.find_one(param)

    def insert_one(self, info):
        """
        插入一条数据
        :param info:
        :return:
        """
        return self.db.insert_one(info)

    def insert_many(self, info):
        """
        插入多条数据
        :param info:
        :return:
        """
        return self.db.insert_many(info)

    def delete_one(self, param):
        """
        删除符合条件的第一条数据
        :param param:
        :return:
        """
        return self.db.delete_one(param)

    def delete_many(self, params):
        """
        删除符合条件的所有数据
        :param params:
        :return:
        """
        return self.db.delete_many(params)

    def update(self, criteria, objNew,):
        """

        :param criteria: 查询条件
        :param objNew: update对象和一些更新操作符
        upsert：如果不存在update的记录，是否插入objNew这个新的文档，true为插入，默认为false，不插入。
        multi：默认是false，只更新找到的第一条记录。如果为true，把按条件查询出来的记录全部更新。

        :return:
        """
        return self.db.update(criteria, objNew, upsert=True, multi=False)


if __name__ == '__main__':
    db = MongoClient('proxy_pool', '127.0.0.1', 27017)
