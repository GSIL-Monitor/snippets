# -*- coding: utf-8 -*-
DEBUG = True

AMQP_CONNECTIONS = {
    'default': 'amqp://127.0.0.1',
}

SQLALCHEMY_ECHO = False
SQLALCHEMY_BINDS = {}
SQLALCHEMY_BINDS['default'] = {
    ''
}
