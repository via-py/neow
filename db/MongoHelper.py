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


if __name__ == '__main__':
    db = MongoClient('proxy_pool', '127.0.0.1', 27017)
