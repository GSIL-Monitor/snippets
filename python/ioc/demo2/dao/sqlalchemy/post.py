# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker

from demo2 import inject

from demo2.dao.post import PostDao
from demo2.model.post import Post


class PostDaoSqlalchemy(PostDao):

    def __init__(self):
        super(PostDaoSqlalchemy, self).__init__()


    def post_construct(self):
        self.session_factory = inject('session_factory', sessionmaker)

    def all(self):
        rv = []
        s = self.session_factory()
        rs = s.execute("SELECT * FROM posts")

        for rows in rs.fetchall():
            m = Post()
            m.id = rows['id']
            m.title = rows['title']
            m.content = rows['content']
            rv.append(m)
        return rv
