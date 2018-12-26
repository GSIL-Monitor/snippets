# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import pprint

# logging.basicConfig(level=logging.CRITICAL)

import jinja2
from qianka.sqlalchemy import QKSQLAlchemy
from sqlalchemy import String, Integer, MetaData, TIMESTAMP
from sqlalchemy.ext.automap import automap_base

from util import config_from_pyfile


config = {}
config.update(config_from_pyfile('config.py'))


db = QKSQLAlchemy()
db.configure(config)

e = db.get_engine()
m = MetaData(bind=e)
m.reflect(only=['user_match'])
base = automap_base(metadata=m)
base.prepare()


_ = base.classes.keys()
print(_)
