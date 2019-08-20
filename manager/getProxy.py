# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :
------------------------------------
@File           :  getProxy.py
@Description    :  从公网获取免费IP-proxy
@CreateTime     :  2019/8/19 16:56
------------------------------------
@ModifyTime     :
@ModifyContent  :
"""
import re
import sys
from utils.RequestUtil import RequestUtil

sys.path.append('..')

# # for debug to disable insecureWarning
# requests.packages.urllib3.disable_warnings()


class GetProxy(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        urls = ['http://www.ip3366.net/free/?stype=1',
                "http://www.ip3366.net/free/?stype=2"]
        request = RequestUtil()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)
                print(proxy)

    @staticmethod
    def freeProxy02():
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        request = RequestUtil()
        for url in urls:
            r = request.get(url, timeout=10)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                yield ":".join(proxy)


if __name__ == '__main__':
    from validator.CheckProxy import CheckProxy

    # CheckProxy.checkAllGetProxyFunc()
    CheckProxy.checkGetProxyFunc(GetProxy.freeProxy01)
