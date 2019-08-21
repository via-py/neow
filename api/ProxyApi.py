# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :
------------------------------------
@File           :  ProxyApi.py
@Description    :  启动Flask接口
@CreateTime     :  2019/8/18 11:48
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import sys
from flask import Flask, Response, jsonify, request
from conf.ConfigGetter import config
from manager.ProxyManager import ProxyManager

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
    proxy = ProxyManager().get()
    return proxy.info_json if proxy else {"code": 0, "src": "no proxy"}


@app.route('/get_all/')
def getAll():
    """
    获取多条IP记录请求
    :return:
    """
    proxies = ProxyManager().getAll()
    return [_.info_dict for _ in proxies]


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
    status = ProxyManager().getNumber()
    return status


@app.route('/delete/', methods=['GET'])
def delete():
    """
    请求删除IP数据记录
    :return:
    """
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return {"code": 0, "src": "success"}


def runFlask():
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    runFlask()
