# -*- coding: utf-8 -*-
import logging
import ioc

from sqlalchemy.orm import sessionmaker

from demo.dao.post import PostDao
from demo.model.post import PostModel


class PostDaoSqlalchemy(PostDao):

    # attrs:
    #   - session_factory

    def __init__(self):
        self.session_factory = None

    def post_construct(self):
        self.session_factory = ioc.inject('db_session_factory', sessionmaker)

    def all(self):
        logging.debug(self.session_factory)
        s = self.session_factory()
        rs = s.execute("SELECT * FROM posts")
        rv = []
        for row in rs.fetchall():
            m = PostModel()
            m.id = row['id']
            m.title = row['title']
            m.content = row['content']
            rv.append(m)
        return rv
