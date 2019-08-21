#-*- coding: utf-8 -*-
'''
---------------

Description of this file

:author: Luopeng
:date created: 2019-08-21
:python version: 3.6

---------------
'''
import sys
from manager.getProxy import GetProxy
from db.RedisHelper import RedisHelper


class Getter():
    def __init__(self):
        self.database = RedisHelper(name='ip_redis')
        self.getter = GetProxy()

    def run(self):
        print('获取器开始执行')
        for callback_label in range(self.getter.__CrawlFuncCount__):
            callback = self.getter.__CrawlFunc__[callback_label]
            # 获取代理
            proxies = self.getter.get_proxies(callback)
            sys.stdout.flush() #刷新缓冲区
            for proxy in proxies:
                self.database.put(name='redis_test', key=proxy[0], value=proxy[1])
                print(proxy, type(proxy[1]), '获取全部IP')

    def get_ips(self):
        ips = self.database.getall(name='redis_test')
        print(ips, "从数据库中获取IP成功")


if __name__ == '__main__':
    A = Getter()
    A.get_ips()
