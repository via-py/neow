# -*- coding: utf-8 -*-
'''
---------------

Description of this file

:author: Luopeng
:date created: 2019-08-21
:python version: 3.6

---------------
'''
import sys
import json
import requests
import random
from manager.getProxy import GetProxy
from db.Redis_test import RedisHelper
from manager.Proxy import Proxy


class Getter():
    def __init__(self):
        self.database = RedisHelper(name='redis_test')
        self.getter = GetProxy()

    def run(self):
        print('获取器开始执行')
        for callback_label in range(self.getter.__CrawlFuncCount__):
            callback = self.getter.__CrawlFunc__[callback_label]
            # 获取代理
            proxies = self.getter.get_proxies(callback)
            sys.stdout.flush()  # 刷新缓冲区
            for proxy in proxies:
                self.database.put(name='redis_test', key=proxy[0], value=proxy[1])
                #print(proxy, type(proxy[1]), '获取全部IP')

    def getter_useful_ips(self):
        ips = self.database.pop(name='available_ips')
        IPAgents = []
        for key, value in ips.items():
            IPAgents.append(value)
        result = random.choice(IPAgents)
        return result


if __name__ == '__main__':
    A = Getter()
    A.getter_useful_ips()
