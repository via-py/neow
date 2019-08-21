#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
    PeriodicTasks.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    :author: fengzf
    :date created: 2019/8/21, 19:42:00
    :python version: 3.6
"""
from conf.ConfigGetter import config
from db import DataStore
from manager import Proxy
from schedule.PeriodicCelery import periodic_inst
from validator.Validator import Validator


@periodic_inst.task(name='task_test')
def test():
    print('hello')


@periodic_inst.task(name='first_verify')
def first_verify_proxy():
    """
    校验初次抓取下来的代理
    :return:
    """
    db = DataStore()
    db.changeTable('raw_proxy')
    if db.getNumber() > 0:
        proxy_json = db.get({})
        proxy_obj = Proxy.newProxyFromJson(proxy_json)
        vp = Validator()
        while True:
            if proxy_obj.fail_count > config.fail_threshold:
                # self.log.error('Fail count is out of threshold, proxy will delete.')
                db.delete(proxy_obj)
                return False
            else:
                if vp.verify(proxy_obj):
                    db.delete(proxy_json)
                    db.changeTable('useful_proxy')
                    db.put(proxy_json)
                    return True


@periodic_inst.task(name='common_verify')
def common_verify_proxy(crontab_time):
    """
    校验未校验过的代理
    :param crontab_time:
    :return:
    """
    db = DataStore()
    db.changeTable('useful_proxy')
    proxy_json = db.get({'last_time': {'$lt': crontab_time}})
    print(proxy_json)
    print(type(proxy_json))
    if proxy_json:
        vp = Validator()
        threshold = 3
        for i in range(threshold):
            if vp.verify(proxy_json):
                return True
    return False


@periodic_inst.task(name='delete_useless')
def delete_useless_proxy():
    """
    定期删除无效代理
    :return:
    """
    db = DataStore()
    db.changeTable('useful_proxy')
    proxies = db.get({'fail_count': {'gt': 9}})
    db.delete(proxies, many=True)

