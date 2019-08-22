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
from schedule.put_proxys import Getter
from validator.Validator import Validator
from validator.CheckProxy import CheckProxy
from manager.getProxy import GetProxy
from schedule.PeriodicCelery import periodic_inst


@periodic_inst.task(name='task_test')
def test():
    print('\t' * 2, '*' * 30)
    print('\t' * 2, '*  ( • ̀ω•́ )-->[ Hello world! ]  *')
    print('\t' * 2, '*' * 30)


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
                vp.log.error('Fail count is out of threshold, proxy will delete.')
                db.delete(proxy_obj.info_dict)
                return False
            else:
                if vp.verify(proxy_obj):
                    db.changeTable('useful_proxy')
                    db.put(proxy_obj.info_dict)
                    db.changeTable('raw_proxy')
                    db.delete(proxy_obj.info_dict)
                    return True


@periodic_inst.task(name='common_verify_all')
def common_verify_all_proxy():
    """
    提出所有ip
    :return:
    """
    db = DataStore()
    db.changeTable('useful_proxy')
    proxies_json = db.getAll()
    for proxy_json in proxies_json:
        proxy_obj = Proxy.newProxyFromJson(proxy_json)
        # 异步执行单个的代理验证，过期时间60秒
        common_verify_proxy.apply_async(args=(proxy_obj, ), exprise=60)
    pass


@periodic_inst.task(name='common_verify')
def common_verify_proxy(proxy_obj):
    """
    校验common_verify_all_proxy中传过来的代理
    :param proxy_obj: 校验对象
    :return:
    """
    db = DataStore()
    if proxy_obj.fail_count > config.fail_threshold:
        db.delete(proxy_obj)
        return False
    else:
        vp = Validator()
        # 线程单次校验次数，后期加入配置中
        threshold = 3
        for i in range(threshold):
            if vp.verify(proxy_obj):
                    return True


# @periodic_inst.task(name='common_verify')
# def common_verify_proxy(crontab_time):
#     """
#     校验common_verify_all_proxy中传过来的代理
#     :param crontab_time: 校验预定开始时间
#     :return:
#     """
#     db = DataStore()
#     db.changeTable('useful_proxy')
#     if config.db_type == 'mongo':
#         proxy_json = db.get({'last_time': {'$lt': crontab_time}})
#     else:
#         proxy_json = db.get({'last_time': {'$lt': crontab_time}})
#     print(proxy_json)
#     print(type(proxy_json))
#     if proxy_json:
#         proxy_obj = Proxy.newProxyFromJson(proxy_json)
#         if proxy_obj.fail_count > config.fail_threshold:
#             db.delete(proxy_obj)
#             return False
#         else:
#             vp = Validator()
#             threshold = 3
#             for i in range(threshold):
#                 if vp.verify(proxy_obj):
#                     return True
#     return False


@periodic_inst.task(name='crawl_proxy')
def crawl_proxy():
    """
    定期爬取代理
    :return:
    """
    # CheckProxy.checkGetProxyFunc(GetProxy.freeProxy01)
    # getter = Getter()
    # getter.get_ips()
    print('get proxy')

