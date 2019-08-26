# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :
------------------------------------
@File           :  ConfigGetter.py
@Description    :  读取setting中的配置
@CreateTime     :  2019/8/18 16:01
------------------------------------
@ModifyTime     :
@ModifyContent  :
"""
from conf.setting import *
from utils.ClassUtil import LazyProperty


class ConfigGetter(object):
    def __init__(self):
        pass

    @LazyProperty
    def db_type(self):
        return DATABASE.get(DB, {}).get('TYPE', 'REDIS')

    @LazyProperty
    def db_name(self):
        return DATABASE.get(DB, {}).get('NAME', 'proxy_pool')

    @LazyProperty
    def db_host(self):
        return DATABASE.get(DB, {}).get('HOST', '127.0.0.1')

    @LazyProperty
    def db_port(self):
        return DATABASE.get(DB, {}).get('PORT', 6379)

    @LazyProperty
    def db_username(self):
        return DATABASE.get(DB, {}).get('USERNAME', '')

    @LazyProperty
    def db_password(self):
        return DATABASE.get(DB, {}).get('PASSWORD', '')

    @LazyProperty
    def table(self):
        return DATABASE.get(DB, {}).get('TABLE', 'useful_proxy')

    @LazyProperty
    def proxy_getter_function(self):
        return PROXY_GETTER

    @LazyProperty
    def host_ip(self):
        return SERVER_API.get('HOST', '127.0.0.1')

    @LazyProperty
    def host_port(self):
        return SERVER_API.get('PORT', 5001)

    @LazyProperty
    def test_url(self):
        return TEST_URL

    @LazyProperty
    def check_count(self):
        return CHECK_COUNT

    @LazyProperty
    def fail_threshold(self):
        return FAIL_THRESHOLD


config = ConfigGetter()

if __name__ == '__main__':
    info = (
        config.db_type,
        config.db_name,
        config.db_host,
        config.db_port,
        config.db_username,
        config.db_password,
        config.host_ip,
        config.host_port,
        config.proxy_getter_function,
        config.table,
    )
    print('{0[0]},{0[1]},{0[2]},{0[3]},'
          '{0[4]},{0[5]},{0[6]},{0[7]},{0[8]},{0[9]},'.format(info))
