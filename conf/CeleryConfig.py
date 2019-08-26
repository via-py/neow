#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
    CeleryConfig.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    
    :author: fengzf
    :date created: 2019/8/20, 14:25:00
    :python version: 3.6
"""
import time

from celery import Celery, platforms
from celery.schedules import crontab


class BaseCeleryConfig(object):
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERYD_CONCURRENCY = 2
    CELERY_ACKS_LATE = True
    CELERY_IGNORE_RESULT = True
    CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_EVENT_QUEUE_EXPIRES = 7200
    CELERY_TIMEZONE = 'UTC'

    BROKER_URL = "amqp://127.0.0.1:5672"
    # BROKER_URL = "redis://127.0.0.1:6379/1"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/2"


class PeriodicCeleryConfig(BaseCeleryConfig):
    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Shanghai'

    """
    导入配置
    """
    CELERY_IMPORTS = (
        # 'schedule.Scheduler',
        'schedule.PeriodicTasks',
    )

    """
    路由配置
    """
    CELERY_ROUTES = {
        'default': {
            'queue': 'default',
            'routing_key': 'default'
        },
        'first_verify': {
            'queue': 'first_verify.queue',
            'routing_key': 'first_verify.queue',
        },
        'common_verify_all': {
            'queue': 'common_verify_all.queue',
            'routing_key': 'common_verify_all.queue',
        },
        'common_verify': {
            'queue': 'common_verify.queue',
            'routing_key': 'common_verify.queue',
        },
        'crawl_proxy': {
            'queue': 'crawl_proxy.queue',
            'routing_key': 'crawl_proxy.queue',
        },
        'test': {
            'queue': 'test.queue',
            'routing_key': 'test.queue',
        },
    }
    CELERY_QUEUES = {
        'default': {
            'exchange': 'default',
            'exchange_type': 'direct',
            'routing_key': 'default',
        },
        'first_verify.queue': {
            'exchange': 'first_verify.queue',
            'exchange_type': 'direct',
            'routing_key': 'first_verify.queue',
        },
        'common_verify_all.queue': {
            'exchange': 'common_verify_all.queue',
            'exchange_type': 'direct',
            'routing_key': 'common_verify_all.queue',
        },
        'common_verify.queue': {
            'exchange': 'common_verify.queue',
            'exchange_type': 'direct',
            'routing_key': 'common_verify.queue',
        },
        'crawl_proxy.queue': {
            'exchange': 'crawl_proxy.queue',
            'exchange_type': 'direct',
            'routing_key': 'crawl_proxy.queue',
        },
        'test.queue': {
            'exchange': 'test.queue',
            'exchange_type': 'direct',
            'routing_key': 'test.queue'
        }
    }

    """
    定时任务配置
    """
    CELERYBEAT_SCHEDULE = {
        'first_verify': {
            # 对应task注册时给的name
            'task': 'first_verify',
            # 一个小时检查一次
            'schedule': crontab(minute=15, hour='*/1'),
            'options': {
                'queue': 'first_verify.queue',
                'routing_key': 'first_verify.queue',
                'exchange': 'first_verify.queue',
                'exchange_type': 'direct'
            }
        },
        'common_verify_all': {
            # 对应task注册时给的name
            'task': 'common_verify_all',
            # 四小时检查一次
            'schedule': crontab(minute=30, hour='*/4'),
            'options': {
                'queue': 'common_verify_all.queue',
                'routing_key': 'common_verify_all.queue',
                'exchange': 'common_verify_all.queue',
                'exchange_type': 'direct'
            },
        },
        'crawl_proxy': {
            # 对应task注册时给的name
            'task': 'crawl_proxy',
            # 'schedule': crontab(minute=45, hour='*/1'),
            'schedule': crontab(minute='*/5',),
            'options': {
                'queue': 'crawl_proxy.queue',
                'routing_key': 'crawl_proxy.queue',
                'exchange': 'crawl_proxy.queue',
                'exchange_type': 'direct'
            }
        },
        'test': {
            # 对应task注册时给的name
            'task': 'task_test',
            'schedule': crontab(minute='*'),
            'options': {
                'queue': 'test.queue',
                'routing_key': 'test.queue',
                'exchange': 'test.queue',
                'exchange_type': 'direct'
            }
        },
    }


def create_celery(name, config):
    inst = Celery(name)
    inst.config_from_object(config)
    platforms.C_FORCE_ROOT = True
    return inst
