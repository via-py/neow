# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :
------------------------------------
@File           :  ProxyApi.py
@Description    :  Flask启动入口
@CreateTime     :  2019/8/18 11:48
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import sys
from flask import Flask, Response, jsonify

sys.path.append('../')

app = Flask(__name__)


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse

api_list = {
    'get': '',
    'get_all': '',
    'delete?num=': '',
    'get_status': ''
}


@app.route('/')
def index():
    """
    请求列表
    :return:
    """
    return api_list


@app.route('/get/')
def get():
    """
    获取单条IP记录请求
    :return:
    """
    return None


@app.route('/get_all/')
def getAll():
    """
    获取多条IP记录请求
    :return:
    """
    return None


@app.route('/refresh/')
def refresh():
    """
    刷新IP记录请求
    :return:
    """
    return None


@app.route('/get_status/')
def getStatus():
    """
    获取IP存活状态
    :return:
    """
    return None


@app.route('/delete/', methods=['GET'])
def delete():
    """
    请求删除IP数据记录
    :return:
    """
    return None


if __name__ == '__main__':
    app.run()
