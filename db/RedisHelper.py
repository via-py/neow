# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  RedisHelper.py
@Description    :  redis操作集合
@CreateTime     :  2019/8/18 17:02
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import re
from random import choice
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

    def get(self, name, key):
        """
        从hash中回去对应的proxy
        :param proxy_str:
        :return:
        """
        return self.__conn.hget(name, key)

    def get_many(self, name, keys, *args):
        """
        批量读取数据属性（没有则新建）
        :param keys:
        :param args:
        :return:
        """
        return self.__conn.hmget(name, keys, *args)

    def put(self, key, value):
        """
        将代理放入hash
        :param proxy_obj: 为一个键值对
        :return:
        """
        return self.__conn.hset(key, value)

    def delete(self, name, *keys):
        """
        移除指定代理
        :param proxy_str:
        :return:
        """
        return self.__conn.hdel(name, *keys)

    def exists(self, name, key):
        """
        判断指定代理是否存在
        :param proxy_str:
        :return:
        """
        try:
            self.__conn.hexists(name, key)
        except Exception:
            print("%s代理不存在" % key)

    def update(self, name, key, value):
        """
        更新proxy属性
        :param proxy_obj:
        :return:
        """
        self.__conn.hset(name, key, value)

    def update_many(self, name, mapping):
        """
        批量更新数据属性，没有则创建
        :param mapping:
        :return:
        """
        return self.__conn.hmset(name, mapping)

    def getall(self, name):
        """
        获取所有代理
        :return:
        """
        try:
            res = self.__conn.hgetall(name)
        except Exception as e:
            print('查询所有hash类型key失败,失败原因:%s' % e)
        else:
            if res:
                new_data = {}
                for k, v in res.items():
                    new_data[k.decode()] = v.decode()
                return new_data

    def pop(self, name):
        """
        弹出一个代理
        :return:
        """
        result = self.__conn.hgetall(name)
        return choice(result)

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


if __name__ == '__main__':
    conn = RedisHelper()
    result = conn.batch(680, 688)
    print(result)