# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  RequestUtil.py
@Description    :  网络请求工具类
@CreateTime     :  2019/8/20 9:12
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
from conf.setting import USER_AGENTS
import random
import requests
import time


class RequestUtil(object):
    def __init__(self, *args, **kwargs):
        pass

    @property
    def user_agent(self):
        """
        Random return of a user_agent
        :return: user_agent
        """
        ua_list = USER_AGENTS
        return random.choice(ua_list)

    @property
    def header(self):
        """
        return header
        :return:
        """
        return {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    def get(self, url, header=None, retry_time=5, timeout=30,
            retry_flag=list(), retry_interval=5, **kwargs):
        """"""
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)

        while True:
            try:
                response = requests.get(url, headers=headers, timeout=timeout, **kwargs)
                print('抓取成功', url, response.status_code)
                if response.status_code == 200:
                    return response.content  # 使用response.text的时候会出现乱码的问题
            except ConnectionError:
                print('抓取失败', url)
                return None

            # try:
            #
            #     html = requests.get(url, header=headers, timeout=timeout, **kwargs)
            #     if any(f in html.content for f in retry_flag):
            #         raise Exception
            #     return html
            # except Exception as e:
            #     # 多次请求
            #     retry_time -= 1
            #     if retry_time <= 0:
            #         resp = requests.Response()
            #         resp.status_code = 200
            #         return resp
            #     time.sleep(retry_interval)
