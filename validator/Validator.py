#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
    Validator.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    :author: fengzf
    :date created: 2019/8/19, 20:04:00
    :python version: 3.6
"""
import time

import requests

from db import DataStore
from manager.Proxy import Proxy
from utils import LogHandler
from conf.ConfigGetter import config


class Validator(object):

    def __init__(self):
        self.conn = DataStore()
        self.log = LogHandler('proxy_validator')
        pass

    def verify(self, proxy_obj):
        """
        验证proxy
        :param proxy_obj: (proxy)
        :return: (bool)
        """
        try:
            self.conn.changeTable('useful_proxy')
            test_url = config.test_url
            self.log.info('Send request to {}.'.format(test_url))
            response = requests.get(test_url, proxies={'http': proxy_obj.proxy})
            self.log.info('Response status code is {}.'.format(response.status_code))
        except:
            self.log.error('Connect failed, fail count: {}.'.format(proxy_obj.fail_count))
            proxy_obj.fail_count += 1
            proxy_obj.check_count += 1
            proxy_obj.last_status = 0
            proxy_obj.last_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            self.conn.update(proxy_obj.proxy, proxy_obj.info_dict)
            return False
        else:
            self.log.info('Connect success.')
            proxy_obj.check_count += 1
            proxy_obj.last_status = 1
            proxy_obj.last_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            self.conn.update(proxy_obj.proxy, proxy_obj.info_dict)
            return True
    pass

