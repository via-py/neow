#-*- coding: utf-8 -*-
'''
---------------

Description of this file

:author: Luopeng
:date created: 2019-08-22
:python version: 3.6

---------------
'''

import asyncio  # 一步io/协程
import aiohttp
import requests

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from db.Redis_test import RedisHelper
from conf.setting import *


# class Tester(object):
#     # def __init__(self):
#     #     self.redis = RedisHelper()
#     @staticmethod
#     async def test_single_proxy(proxy):
#         """
#         测试单个代理
#         :param proxy:
#         :return:
#         """
#         conn = aiohttp.TCPConnector(verify_ssl=False)
#         async with aiohttp.ClientSession(connector=conn) as session:
#             try:
#                 if isinstance(proxy, bytes):
#                     proxy = proxy.decode('utf-8')
#                 real_proxy = 'http://' + proxy
#                 print('正在测试', proxy)
#                 async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
#                     if response.status == 200:
#                         # self.redis.max(proxy)
#                         print('代理可用', proxy)
#                     else:
#                         # self.redis.decrease(proxy)
#                         print('请求响应码不合法 ', response.status, 'IP', proxy)
#             except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
#                 # self.redis.decrease(proxy)
#                 print('代理请求失败', proxy)


async def test_single_proxy(proxy):
    """
    #         测试单个代理
    #         :param proxy:
    #         :return:
            """
    redis = RedisHelper('available_ips')
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://' + proxy
            print('正在测试', proxy)
            async with session.get(TEST_URL, proxy=real_proxy, timeout=1, allow_redirects=False) as response:
                if response.status == 200:
                    ip = proxy.split(':')[:1]
                    key = str(ip)
                    value = proxy
                    redis_info = redis.getall(name='available_ips')
                    if key not in redis_info.keys():
                        redis.put(name='available_ips', key=key, value=value)
                    print('---***---存储成功---****---')
                else:
                    print('请求响应码不合法 ', response.status, 'IP', proxy)
        except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
            print('代理请求失败', proxy)


def run():
    redis = RedisHelper('redis_test')
    ips = redis.getall(name='redis_test')
    IPAgents = []
    for key, value in ips.items():
        print(value, 'ip地址')
        IPAgents.append(value)
    # 增加重试连接次数
    requests.adapters.DEFAULT_RETRIES = 3
    for IP in IPAgents:
        coroutine = test_single_proxy(IP)
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(coroutine)
        loop.run_until_complete(task)


if __name__ == '__main__':
    run()




