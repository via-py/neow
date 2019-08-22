# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  RedisHelper.py
@Description    :  封装redis操作工具类接口
@CreateTime     :  2019/8/18 17:02
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import random
from redis import Redis, BlockingConnectionPool
from conf.setting import PY3


class RedisHelper(object):
    """
    Redis中代理存放的结构为hash：
        原始代理存放在name为raw_proxy的hash中, key为代理的ip:por, value为代理属性的字典;
        验证后的代理存放在name为useful_proxy的hash中, key为代理的ip:port, value为代理属性的字典;

    """

    def __init__(self, name, **kwargs):
        """
        init
        :param name: hash name
        :param host: host
        :param port: port
        :param password: password
        :return:
        """
        self.name = name
        self.__conn = Redis(connection_pool=BlockingConnectionPool(**kwargs))

    def changeTable(self, name):
        """
        切换操作对象
        :param name: raw_proxy/useful_proxy
        :return:
        """
        self.name = name

    def get(self, proxy_str):
        """
        从hash中获取对应的proxy, 使用前需要调用changeTable()
        :param proxy_str: proxy str
        :return:
        """
        data = self.__conn.hget(name=self.name, key=proxy_str)
        if data:
            return data.decode('utf-8') if PY3 else data
        else:
            return None

    def put(self, proxy_obj):
        """
        将代理放入hash, 使用changeTable指定hash name
        :param proxy_obj: Proxy obj
        :return:
        """
        data = self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.info_json)
        return data

    def delete(self, proxy_str):
        """
        移除指定代理, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        self.__conn.hdel(self.name, proxy_str)

    def exists(self, proxy_str):
        """
        判断指定代理是否存在, 使用changeTable指定hash name
        :param proxy_str: proxy str
        :return:
        """
        return self.__conn.hexists(self.name, proxy_str)

    def update(self, proxy_obj):
        """
        更新 proxy 属性
        :param proxy_obj:
        :return:
        """
        self.__conn.hset(self.name, proxy_obj.proxy, proxy_obj.info_json)

    def pop(self):
        """
        返回并删除一个proxy信息
        :return: dict {proxy: value}
        """
        proxies = self.__conn.hkeys(self.name)
        if proxies:
            proxy = random.choice(proxies)
            value = self.__conn.hget(self.name, proxy)
            self.delete(proxy)
            return {'proxy': proxy.decode('utf-8') if PY3 else proxy,
                    'value': value.decode('utf-8') if PY3 and value else value}
        return None

    def getAll(self, name):
        """
        列表形式返回所有代理, 使用changeTable指定hash name
        :return:
        """
        item_dict = self.__conn.hgetall(name)
        if PY3:
            return [value.decode('utf8') for key, value in item_dict.items()]
        else:
            return item_dict.values()

    def clean(self):
        """
        清空所有代理, 使用changeTable指定hash name
        :return:
        """
        return self.__conn.delete(self.name)

    def getNumber(self):
        """
        返回代理数量
        :return:
        """
        return self.__conn.hlen(self.name)
