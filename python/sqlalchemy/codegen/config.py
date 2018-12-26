# -*- coding: utf-8 -*-
DEBUG = True

SQLALCHEMY_ECHO = False
SQLALCHEMY_LOGGING = False

SQLALCHEMY_BINDS = {}
SQLALCHEMY_BINDS['default'] = {}
SQLALCHEMY_BINDS['default']['adapter'] = 'mysql'
SQLALCHEMY_BINDS['default']['connector'] = 'mysqldb'
SQLALCHEMY_BINDS['default']['host'] = (
    'rdsnrm3ayarjnei391.mysql.rds.aliyuncs.com')
SQLALCHEMY_BINDS['default']['port'] = 3306
SQLALCHEMY_BINDS['default']['user'] = 'hera_web'
SQLALCHEMY_BINDS['default']['pwd'] = 'Jks8DjWa'
SQLALCHEMY_BINDS['default']['db'] = 'zhuanqian'
SQLALCHEMY_BINDS['default']['charset'] = 'utf8'
