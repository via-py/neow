# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  ProxyManager.py
@Description    :  
@CreateTime     :  2019/8/19 11:02
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
from db import DataStore


class ProxyManager(object):
    def __init__(self):
        self.db = DataStore()
        self.raw_proxy_queue = 'raw_proxy'
        self.useful_proxy_queue = 'useful_proxy'
