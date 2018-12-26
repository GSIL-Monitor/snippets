# -*- coding: utf-8 -*-
from flask import Config

from qianka.sqlalchemy import QKSQLAlchemy
db = QKSQLAlchemy()

config = Config('.')

config.from_pyfile('config.py')

db.configure(config)
