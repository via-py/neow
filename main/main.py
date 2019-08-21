# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zzmi
@Version        :  
------------------------------------
@File           :  main.py
@Description    :  接口调度主要程序入口
@CreateTime     :  2019/8/21 19:42
------------------------------------
@ModifyTime     :  
@ModifyContent  :  
"""
import sys
import signal
from multiprocessing import Process
from api.ProxyApi import runFlask as ProxyApiRun

sys.path.append('.')
sys.path.append('..')


def run():
    p_list = list()
    p1 = Process(target=ProxyApiRun, name='ProxyApiRun')
    p_list.append(p1)
    # TODO: 还需要实现"检验proxy的调度实例"和"刷新proxy的调度实例"

    def kill_child_processes(signum, frame):
        for p in p_list:
            p.terminate()
        sys.exit(1)

    signal.signal(signal.SIGTERM, kill_child_processes)

    for p in p_list:
        p.daemon = True
        p.start()
    for p in p_list:
        p.join()


if __name__ == '__main__':
    run()
