# -*- coding: utf-8 -*-

#
# - development
# - test
# - production
#
ENV = 'development'

DEBUG = True

#
# machine_id
#
MACHINE_ID = '99'

# domain config
KAGOU_API_DOMAIN = 'http://feature_cp_api.api.test.kagou.me'

#
# dconfig
#
DCONFIG_FILE = '/path/to/non-exists-file'
DCONFIG_TIMEOUT = 60

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dbaroot@172.16.3.234/chengpin?charset=utf8'
SQLALCHEMY_BINDS = {
    'default': 'mysql+pymysql://dbaroot@172.16.3.234/chengpin?charset=utf8',
}
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@127.0.0.1/chengpin?charset=utf8'
# SQLALCHEMY_BINDS = {
#     'default': 'mysql+pymysql://root@127.0.0.1/chengpin?charset=utf8',
# }

#
# redis
#
REDIS_BINDS = {
    'default': 'redis://'
}

#
# sessions
#
SECRET_KEY = 'all your base are belong to us'
SESSION_COOKIE_NAME = 'demo_session'
# PERMANENT_SESSION_LIFETIME = 7200
SESSION_REDIS = 'redis://172.16.3.234'
# SESSION_REDIS = 'redis://'
SESSION_REDIS_PREFIX = 'demo_session:'

#
# assets
#

ASSETS_DEBUG = True

CDN_ASSETS_PREFIX = 'http://c.qkcdn.com'

#
# url
#
API_PREFIX = '/api'
