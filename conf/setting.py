# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :
------------------------------------
@File           :  setting.py
@Description    :  全局配置文件
@CreateTime     :  2019/8/18 15:44
------------------------------------
@ModifyTime     :
@ModifyContent  :
"""
import sys
from os import getenv
from logging import getLogger
from manager.getProxy import GetProxy

log = getLogger(__name__)

PY3 = sys.version_info >= (3,)

DB = 'mongo'
DB_TYPE = getenv('db_type', 'REDIS').upper()
DB_HOST = getenv('db_host', '127.0.0.1')
DB_PORT = getenv('db_port', '6379')
DB_NAME = getenv('db_name', 'proxy_pool')
DB_USERNAME = getenv('db_username', '')
DB_PASSWORD = getenv('db_password', '')

""" 数据库配置 """
DATABASE = {
    "default": {
        "ENGINE": '',
        "TYPE": DB_TYPE,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        # "NAME": DB_NAME,
        # "USERNAME": DB_USERNAME,
        "PASSWORD": DB_PASSWORD,
        "TABLE": 'raw_proxy',
    },
    "mongo": {
        "ENGINE": '',
        "TYPE": 'MONGODB',
        "HOST": DB_HOST,
        "PORT": 27017,
        "NAME": 'proxy_pool',
        "USERNAME": '',
        "PASSWORD": '',
        "TABLE": 'raw_proxy',
    },
}

# 验证次数

FAIL_THRESHOLD = 10
TEST_URL = "https://www.baidu.com"

SERVER_API = {
    "HOST": '0.0.0.0',
    "PORT": 5001
}

# register the proxy getter function
PROXY_GETTER = [
    "crawl_daili66", "crawl_ip3366", "crawl_89ip",
    "crawl_kxdaili", "crawl_kuaidaili"
]

""" API config http://127.0.0.1:5010 """
SERVER_API = {
    "HOST": "0.0.0.0",  # The ip specified which starting the web API
    "PORT": 5010  # port number to which the server listens to
}


class ConfigError(BaseException):
    pass


def checkConfig():
    if DB_TYPE not in ['REDIS', 'MONGODB']:
        raise ConfigError("db_type don't support: %s, must REDIS/MONGODB." % DB_TYPE)

    if not DB_PORT.isdigit():
        raise ConfigError("db_port must be digit, not %s" % DB_PORT)

    illegal_getter = list(filter(lambda key: not hasattr(GetProxy, key), PROXY_GETTER))
    if len(illegal_getter) > 0:
        raise ConfigError("ProxyGetter: %s doesn't exists" % "/".join(illegal_getter))


checkConfig()
