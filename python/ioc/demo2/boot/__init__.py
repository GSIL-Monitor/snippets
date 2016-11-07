# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from demo2.dao.sqlalchemy.post import PostDaoSqlalchemy
from demo2.repo.post import PostRepo
from demo2.domain.post import PostDomain
from demo2.web import WebApp

beans = {}

def boot():
    global beans

    engine = create_engine(
        'sqlite:///test.db',
        echo=True)

    beans['session_factory'] = sessionmaker(
        engine, autocommit=True, autoflush=True)

    beans['PostDao'] = PostDaoSqlalchemy()
    beans['PostRepo'] = PostRepo()
    beans['PostDomain'] = PostDomain()
    _ = WebApp('demo2')
    beans['WebApp'] = _

    for b in beans.values():
        if hasattr(b, 'post_construct'):
            b.post_construct()
