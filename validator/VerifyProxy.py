#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
    VerifyProxy.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    :author: fengzf
    :date created: 2019/8/19, 20:04:00
    :python version: 3.6
"""
from datetime import datetime

import requests

from db import DataStore
from manager.Proxy import Proxy


class ValidatorProxy(object):

    def __init__(self):
        self.conn = DataStore()
        pass

    def have_proxy(self):
        self.conn.changeTable('useful_proxy')
        if self.conn.getNumber():
            return True
        return False

    def validator_one(self, proxy_json):
        if proxy_json:
            proxy = Proxy.newProxyFromJson(proxy_json)
            try:
                requests.get('https://www.baidu.com', proxies={'http': proxy.proxy})
            except:
                print('connect failed')
                proxy.fail_count += 1
                proxy.check_count += 1
                proxy.last_status = 0
                proxy.last_time = datetime.utcnow()
                self.conn.update(proxy_json, proxy.info_json)
                return False
            else:
                print('connect success')
                proxy.check_count = 0
                proxy.last_status = 1
                proxy.last_time = datetime.utcnow()
                self.conn.update(proxy_json, proxy.info_json)
                return True
        pass
    pass

