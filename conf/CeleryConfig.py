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

from celery import Celery
from celery.schedules import crontab
from kombu import Exchange, Queue


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


class ScheduleCeleryConfig(BaseCeleryConfig):
    CELERY_IMPORTS = (
        'test.test_celery'
    )

    CELERY_ROUTES = {
        'default': {
            'queue': 'default',
            'routing_key': 'default'
        },
        'validator': {
            'queue': 'validator.queue',
            'routing_key': 'validator.queue',
        },
        'crawler': {
            'queue': 'crawler.queue',
            'routing_key': 'crawler.queue',
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
        'validator.queue': {
            'exchange': 'validator.queue',
            'exchange_type': 'direct',
            'routing_key': 'validator.queue',
        },
        'crawler.queue': {
            'exchange': 'crawler.queue',
            'exchange_type': 'direct',
            'routing_key': 'crawler.queue',
        },
        'test.queue': {
            'exchange': 'test.queue',
            'exchange_type': 'direct',
            'routing_key': 'test.queue'
        }
    }


class PeriodicCeleryConfig(BaseCeleryConfig):
    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Shanghai'

    """
    导入配置
    """
    CELERY_IMPORTS = (
        'schedule.Scheduler',
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
        'common_verify': {
            'queue': 'common_verify.queue',
            'routing_key': 'common_verify.queue',
        },
        'delete_useless': {
            'queue': 'delete_useless.queue',
            'routing_key': 'delete_useless.queue',
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
        'common_verify.queue': {
            'exchange': 'common_verify.queue',
            'exchange_type': 'direct',
            'routing_key': 'common_verify.queue',
        },
        'delete_useless.queue': {
            'exchange': 'delete_useless.queue',
            'exchange_type': 'direct',
            'routing_key': 'delete_useless.queue',
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
            'schedule': crontab(minute=30, hour='*/1'),
            'options': {
                'queue': 'first_verify.queue',
                'routing_key': 'first_verify.queue',
                'exchange': 'first_verify.queue',
                'exchange_type': 'direct'
            }
        },
        'common_verify': {
            # 对应task注册时给的name
            'task': 'common_verify',
            # 四小时检查一次
            'schedule': crontab(minute=15, hour='*/4'),
            'options': {
                'queue': 'common_verify.queue',
                'routing_key': 'common_verify.queue',
                'exchange': 'common_verify.queue',
                'exchange_type': 'direct'
            },
            'args': (time.strftime('%Y%m%d%H%M%S', time.localtime()))
        },
        'delete_useless': {
            # 对应task注册时给的name
            'task': 'delete_useless',
            'schedule': crontab(minute=45, hour='*/4'),
            'options': {
                'queue': 'delete_useless.queue',
                'routing_key': 'delete_useless.queue',
                'exchange': 'delete_useless.queue',
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
    inst.C_FORCE_ROOT = True
    return inst
