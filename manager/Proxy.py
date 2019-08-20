# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  Proxy.py
@Description    :  初始化Proxy类
@CreateTime     :  2019/8/19 11:03
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import json


class Proxy(object):
    def __init__(self, proxy, fail_count=0, region="",
                 proxy_type="", source="", check_count=0,
                 last_status="", last_time=""):
        self._proxy = proxy
        self._fail_count = fail_count
        self._region = region
        self._proxy_type = proxy_type
        self._source = source
        self._check_count = check_count
        self._last_status = last_status
        self._last_time = last_time

    @classmethod
    def newProxyFromJson(cls, proxy_json):
        """
        根据proxy属性创建Proxy实例
        :param proxy_json:
        :return:
        """
        proxy_dict = json.loads(proxy_json)
        return cls(proxy=proxy_dict.get('proxy', ''),
                   fail_count=proxy_dict.get('fail_count', 0),
                   region=proxy_dict.get('region', ''),
                   proxy_type=proxy_dict.get('proxy_type', ''),
                   source=proxy_dict.get('source', ''),
                   check_count=proxy_dict.get('check_count', 0),
                   last_status=proxy_dict.get('last_status', ''),
                   last_time=proxy_dict.get('last_time', ''))

    @property
    def proxy(self):
        """
        代理 ip:port
        :return:
        """
        return self._proxy

    @property
    def fail_count(self):
        """
        检测失败的次数
        :return:
        """
        return self._fail_count

    @property
    def region(self):
        """
        IP地理位置【国家/城市】
        :return:
        """
        return self._region

    @property
    def proxy_type(self):
        """
        【透明/匿名/高匿】
        :return:
        """
        return self._proxy_type

    @property
    def source(self):
        """
        来源
        :return:
        """
        return self._source

    @property
    def check_count(self):
        """
        检测次数
        :return:
        """
        return self._check_count

    @property
    def last_status(self):
        """
        最后一次检测结果【0：不可用；1：可用】
        :return:
        """
        return self._last_status

    @property
    def last_time(self):
        """
        最后一次检测时间
        :return:
        """
        return self._last_time

    @property
    def info_dict(self):
        """
        属性字典
        :return:
        """
        return {'proxy': self._proxy,
                'fail_count': self._fail_count,
                'region': self._region,
                'proxy_type': self._proxy_type,
                'source': self._source,
                'check_count': self._check_count,
                'last_status': self._last_status,
                'last_time': self._last_time}

    @property
    def info_json(self):
        """
        属性的json格式
        :return:
        """
        return json.dumps(self.info_dict, ensure_ascii=False)

    @fail_count.setter
    def fail_count(self, value):
        self._fail_count = value

    @region.setter
    def region(self, value):
        self._region = value

    @proxy_type.setter
    def proxy_type(self, value):
        self._proxy_type = value

    @source.setter
    def source(self, value):
        self._source = value

    @check_count.setter
    def check_count(self, value):
        self._check_count = value

    @last_status.setter
    def last_status(self, value):
        self._last_status = value

    @last_time.setter
    def last_time(self, value):
        self._last_time = value
