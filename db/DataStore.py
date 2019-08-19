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
    DataStore DB工厂类
      提供get/put/update/pop/delete/exists/getAll/clean/getNumber/changeTable方法

    目前存放代理的有两种, 使用changeTable方法切换操作对象：
      raw_proxy： 存放原始的代理；
      useful_proxy： 存放检验后的代理；

    抽象方法定义：
        get(proxy): 返回指定proxy的信息;
        put(proxy): 存入一个proxy信息;
        pop(): 返回并删除一个proxy信息;
        update(proxy): 更新指定proxy信息;
        delete(proxy): 删除指定proxy;
        exists(proxy): 判断指定proxy是否存在;
        getAll(): 列表形式返回所有代理;
        clean(): 清除所有proxy信息;
        getNumber(): 返回proxy数据量;
        changeTable(name): 切换操作对象 raw_proxy/useful_proxy

    所有方法需要相应类去具体实现：
        redis: RedisHelper.py
        mongodb: MongoHelper.py
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
