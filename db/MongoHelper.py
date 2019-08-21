# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  MongoHelper.py
@Description    :  封装mongodb操作工具类接口
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

    def changeTable(self, name):
        """
        切换操作对象
        :param name:
        :return:
        """
        self.name = name

    def get(self, proxy):
        """
        从hash中获取对应的proxy, 使用前需要调用changeTable()
        :param proxy:
        :return:
        """
        data = self.db[self.name].find_one({'proxy': proxy})
        return data['num'] if data is not None else None

    def put(self, proxy, num=1):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy:
        :param num:
        :return:
        """
        if self.db[self.name].find_one({'proxy': proxy}):
            return None
        else:
            self.db[self.name].insert({'proxy': proxy, 'num': num})

    def pop(self):
        """
        返回并删除一个proxy信息
        :return:
        """
        data = list(self.db[self.name].aggregate([{'$sample': {'size': 1}}]))
        if data:
            data = data[0]
            value = data['proxy']
            self.delete(value)
            return {'proxy': value, 'value': data['num']}
        return None

    def delete(self, value):
        """
        移除指定代理, 使用changeTable指定hash name
        :param value:
        :return:
        """
        self.db[self.name].remove({'proxy': value})

    def exists(self, key):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param key:
        :return:
        """
        return True if self.db[self.name].find_one({'proxy': key}) is not None else False

    def update(self, key, value):
        """
        更新 proxy 属性
        :param key:
        :param value:
        :return:
        """
        self.db[self.name].update({'proxy': key}, {'$inc': {'num': value}})

    def getAll(self):
        """
        列表形式返回所有代理, 使用changeTable指定hash name
        :return:
        """
        return {p['proxy']: p['num'] for p in self.db[self.name].find()}

    def clean(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        self.client.drop_database('proxy')

    def delete_all(self):
        """
        删除存储库
        :return:
        """
        self.db[self.name].remove()

    def getNumber(self):
        """
        返回代理数量
        :return:
        """
        return self.db[self.name].count()
