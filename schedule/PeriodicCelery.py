#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
    PeriodicCelery.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    :author: fengzf
    :date created: 2019/8/21, 19:54:00
    :python version: 3.6
"""
from conf.CeleryConfig import create_celery, PeriodicCeleryConfig

periodic_inst = create_celery(name='periodic_celery', config=PeriodicCeleryConfig)
