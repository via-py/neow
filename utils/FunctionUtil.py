# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  FunctionUtil.py
@Description    :  校验工具类
@CreateTime     :  2019/8/20 9:35
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import re


def verifyProxyFormat(proxy):
    """
    校验代理格式
    :param proxy:
    :return:
    """
    verify_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'
    _proxy = re.findall(verify_regex, proxy)
    return True if len(proxy) == 1 and _proxy[0] == proxy else False
