# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  ProxyManager.py
@Description    :  从数据库中获取ip_proxy
@CreateTime     :  2019/8/19 11:02
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
from db.DataStore import DataStore
from utils.LogHandler import LogHandler
from conf.ConfigGetter import config
from manager.getProxy import GetProxy
from utils.FunctionUtil import verifyProxyFormat
from manager.Proxy import Proxy
import random


class ProxyManager(object):
    def __init__(self):
        self.db = DataStore()
        self.raw_proxy_queue = 'raw_proxy'
        self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy'

    def fetch(self):
        """
        fetch proxy into db by ProxyGetter
        :return:
        """
        self.db.changeTable(self.raw_proxy_queue)
        proxy_set = set()
        self.log.info('ProxyFetch：start')
        for proxyGetter in config.proxy_getter_function:
            self.log.info('ProxyFetch - {func}：start'.format(func=proxyGetter))
            try:
                for proxy in getattr(GetProxy, proxyGetter.strip())():
                    proxy = proxy.strip()

                    if not proxy or not verifyProxyFormat(proxy):
                        self.log.error('ProxyFetch - {func}:{proxy} illegal'.format(func=proxyGetter, proxy=proxy.ljust(20)))
                        continue
                    elif proxy in proxy_set:
                        self.log.info('ProxyFetch - {func}:{proxy} exist'.format(func=proxyGetter, proxy=proxy.ljust(20)))
                        continue
                    else:
                        self.log.info('ProxyFetch - {func}:{proxy} success'.format(func=proxyGetter, proxy=proxy.ljust(20)))
                        self.db.put(Proxy(proxy, source=proxyGetter))
                        proxy_set.add(proxy)
            except Exception as e:
                self.log.error('ProxyFetch - {func}: error'.format(func=proxyGetter))
                self.log.error(str(e))

    def get(self):
        """
        return a useful proxy
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_list = self.db.getAll()
        if item_list:
            random_choice = random.choice(item_list)
            return Proxy.newProxyFromJson(random_choice)
        return None

    def delete(self, proxy_str):
        """
        delete proxy from pool
        :param proxy_str:
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy_str)

    def getAll(self):
        """
        get all proxy from pool
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_list = self.db.getAll()
        return [Proxy.newProxyFromJson(i) for i in item_list]

    def getNumber(self):
        """
        get the number proxy from pool
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.changeTable(self.raw_proxy_queue)
        total_useful_queue = self.db.getNumber()
        total_raw_proxy = self.db.getNumber()
        return {'raw_proxy': total_raw_proxy, 'useful_queue': total_useful_queue}


if __name__ == '__main__':
    pm = ProxyManager()
    pm.fetch()
