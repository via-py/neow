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
from manager.getProxy import GetProxy
from db.Redis_test import RedisHelper
from manager.Proxy import Proxy


class Proxy(object):

    def __init__(self, proxy, info_json):
        self.proxy = proxy,
        self.info_json = info_json

class ProxyInfo(Proxy):
    def __init__(self):
        Proxy.__init__(self)


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
                print(proxy, type(proxy[1]), '获取全部IP')
                print('存储成功')

    def get_ips(self):
        ips = self.database.getall(name='redis_test')
        print(ips, '打印ips')
        IPAgents = []
        for key, value in ips.items():
            print(value, 'ip地址')
            IPAgents.append(value)
        # 增加重试连接次数
        requests.adapters.DEFAULT_RETRIES = 3
        for IP in IPAgents:
            try:
                thiProxy = "http://" + IP
                response = requests.get(url="http://icanhazip.com/", timeout=1, proxies={"http": thiProxy})
                if (response.status_code == 200):
                    print("代理IP:'" + IP + "'有效！")
                else:
                    print("代理IP无效！")
            except:
                print("代理IP无效！")


if __name__ == '__main__':
    A = Getter()
    A.get_ips()
