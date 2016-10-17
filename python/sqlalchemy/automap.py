# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.automap import automap_base

engine = create_engine('mysql+pymysql://root@127.0.0.1/mysql')

meta = MetaData(bind=engine)

meta.reflect(only=['user'])

Base = automap_base(metadata=meta)

Base.prepare()

User = Base.classes.user

print(getattr(User.classes, 'user'))
print(User)
print(User.__table__)
