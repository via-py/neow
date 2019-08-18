# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  RedisHelper.py
@Description    :
@CreateTime     :  2019/8/18 17:02
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
from redis import Redis, BlockingConnectionPool


class RedisHelper(object):
    """
    Redis存放
    """
    def __init__(self, name, **kwargs):
        """
        init初始化
        :param name:
        :param kwargs:
        """
        self.name = name
        self.__conn = Redis(connection_pool=BlockingConnectionPool(**kwargs))

    def get(self, proxy_str):
        """
        从hash中回去对应的proxy
        :param proxy_str:
        :return:
        """
        pass

    def put(self, proxy_obj):
        """
        将代理放入hash
        :param proxy_obj:
        :return:
        """
        pass

    def delete(self, proxy_str):
        """
        移除指定代理
        :param proxy_str:
        :return:
        """
        pass

    def exists(self, proxy_str):
        """
        判断指定代理是否存在
        :param proxy_str:
        :return:
        """
        pass

    def update(self, proxy_obj):
        """
        更新proxy属性
        :param proxy_obj:
        :return:
        """
        pass

    def pop(self):
        """
        弹出一个代理
        :return:
        """
        pass

    def getall(self):
        """
        获取所有代理
        :return:
        """
        pass

    def clear(self):
        """
        清空所有代理
        :return:
        """
        pass

    def getNumber(self):
        """
        切换操作对象
        :return:
        """
        pass
