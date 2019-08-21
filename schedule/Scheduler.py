#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
    Scheduler.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    :author: fengzf
    :date created: 2019/8/20, 15:03:00
    :python version: 3.6
"""
# from gevent import monkey
# monkey.patch_all()
import sys
import os

from db import DataStore
from manager import Proxy
from validator.VerifyProxy import ValidatorProxy

from celery import Celery, platforms
from celery.schedules import crontab

from conf.CeleryConfig import PeriodicCeleryConfig

sys.path.append(os.getcwd())

app = Celery('default_test_celery')
app.config_from_object(PeriodicCeleryConfig)
# platforms.C_FORCE_ROOT = True  # running celery worker by rooter


@app.task(name='task_test')
def test():
    print('hello')


@app.task(name='first_verify')
def first_verify_proxy():
    db = DataStore()
    db.changeTable('raw_proxy')
    print(db.getNumber())
    if db.getNumber() > 0:
        proxy_json = db.get({})
        print(proxy_json)
        vp = ValidatorProxy()
        threshold = 3
        for i in range(threshold):
            if vp.validator_one(proxy_json):
                db.delete(proxy_json)
                db.changeTable('useful_proxy')
                db.put(proxy_json)
                return True
        db.delete(proxy_json)
        return False


@app.task(name='common_verify')
def common_verify_proxy(utctime):
    db = DataStore()
    db.changeTable('useful_proxy')
    proxy_json = db.get({'last_time': {'$lt': utctime}})
    if proxy_json:
        vp = ValidatorProxy()
        threshold = 3
        for i in range(threshold):
            if vp.validator_one(proxy_json):
                return True
    return False


@app.task(name='delete_useless')
def delete_useless_proxy():
    db = DataStore()
    db.changeTable('useful_proxy')
    proxies = db.get({'fail_count': {'gt': 9}})
    db.delete(proxies, many=True)


