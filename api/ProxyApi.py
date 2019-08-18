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


@app.route('/')
def hello_world():
    return 'Start-up Test!!!'


if __name__ == '__main__':
    app.run()
