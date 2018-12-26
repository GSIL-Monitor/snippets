# -*- coding: utf-8 -*-

from kombu import Exchange, Queue

# BROKER_URL = 'amqp://guest:guest@127.0.0.1:5672//'
BROKER_URL = 'redis://'
CELERY_IGNORE_RESULT = True
CELERY_CREATE_MISSING_QUEUES = False
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_DELIVERY_MODE = 'transient'
CELERY_RESULT_EXCHANGE = 'celery.result'
CELERY_RESULT_PERSISTENT = False

CELERY_QUEUES = (
    Queue(
        'default', Exchange('default'), routing_key='default',
        durable=False, auto_delete=True),
)


config = {
    'BROKER_URL': BROKER_URL,
    'CELERY_IGNORE_RESULT': True,
    'CELERY_CREATE_MISSING_QUEUES': False,
    'CELERY_DEFAULT_QUEUE': 'default',
    'CELERY_DEFAULT_EXCHANGE': 'default',
    'CELERY_DEFAULT_EXCHANGE_TYPE': 'direct',
    'CELERY_DEFAULT_DELIVERY_MODE': 'transient',
    'CELERY_QUEUES': CELERY_QUEUES,
    'CELERY_RESULT_EXCHANGE': CELERY_RESULT_EXCHANGE,
    'CELERY_RESULT_PERSISTENT': False,
}
