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
import json
import random

from pymongo import MongoClient

from conf.setting import DB_NAME


class MongoHelper(object):

    def __init__(self, name, host, port, **kwargs):
        self.name = name
        self.client = MongoClient(host, port, **kwargs)
        self.db = self.client[DB_NAME]

    def changeTable(self, name):
        """
        切换操作对象
        :param name:
        :return:
        """
        self.name = name

    def get(self, proxy_str):
        """
        从hash中获取对应的proxy, 使用前需要调用changeTable()
        :param proxy_str: proxy.proxy 属性(ip:port)
        :return:str: json 字符串
        """
        data = self.db[self.name].find_one({'proxy': proxy_str})
        del(data['_id'])
        return json.dumps(data) if data else None

    def put(self, proxy_obj):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy_obj: proxy 对象
        :return:
        """
        if self.db[self.name].find_one({'proxy': proxy_obj.proxy}):
            self.update(proxy_obj)
        else:
            self.db[self.name].insert(proxy_obj.info_dict)

    def pop(self):
        """
        返回并删除一个proxy信息
        :return: proxy_json
        """
        proxies = self.getAll()
        if proxies:
            proxy_json = random.choice(proxies)
            proxy_str = json.loads(proxy_json)['proxy']
            self.delete(proxy_str)
            return proxy_json
        return None

    def delete(self, proxy_str):
        """
        移除指定代理, 使用changeTable指定hash name
        :param proxy_str:
        :return:
        """
        self.db[self.name].remove({'proxy': proxy_str})

    def exists(self, proxy_str):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param proxy_str:
        :return:
        """
        return True if self.db[self.name].find_one({'proxy': proxy_str}) else False

    def update(self, proxy_obj):
        """
        更新 proxy 属性
        :param proxy_obj:
        :return:
        """
        self.db[self.name].update({'proxy': proxy_obj.proxy}, {'$set': proxy_obj.info_dict})

    def getAll(self):
        """
        列表形式返回所有代理, 使用changeTable指定hash name
        :return:
        """
        proxies_json = []
        for proxy in self.db[self.name].find():
            del(proxy['_id'])
            proxies_json.append(json.dumps(proxy))
        return proxies_json

    def clean(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        self.client.drop_database(DB_NAME)

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
