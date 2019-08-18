# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  DataStore.py
@Description    :
@CreateTime     :  2019/8/18 16:46
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import os
import sys
from conf.ConfigGetter import config
from utils.ClassUtil import Singleton

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class DataStore(object):
    """
    sql存储
    """
    __metaclass__ = Singleton

    def __int__(self):
        self.__initDB()

    def __initDB(self):
        """
        init DB
        :return:
        """
        __type = None
        if "REDIS" == config.db_type:
            __type = 'RedisHelper'
        elif 'MONGODBB' == config.db_type:
            __type = 'MongoHelper'
        else:
            pass
        assert __type, 'type error, Not support DB type: {}'.format(config.db_type)
        self.client = getattr(__import__(__type), __type)(name=config.db_name,
                                                          host=config.db_host,
                                                          port=config.db_port,
                                                          password=config.db_password)

    def get(self, key, **kwargs):
        return self.client.get(key, **kwargs)

    def put(self, key, **kwargs):
        return self.client.put(key, **kwargs)

    def update(self, key, value, **kwargs):
        return self.client.update(key, value, **kwargs)

    def delete(self, key, **kwargs):
        return self.client.delete(key, **kwargs)

    def exists(self, key, **kwargs):
        return self.client.exists(key, **kwargs)

    def pop(self, **kwargs):
        return self.client.pop(**kwargs)

    def getAll(self):
        return self.client.getAll()

    def clear(self):
        return self.client.clear()

    def changeTable(self, name):
        self.client.changeTable(name)

    def getNumber(self):
        return self.client.getNumber()
