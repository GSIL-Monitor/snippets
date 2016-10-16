# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ioc
from ioc.decorators import Bean

from demo.domain.post import PostDomain
from demo.repo.post import PostRepo
from demo.dao.sqlalchemy.post import PostDaoSqlalchemy

class MyConfig(ioc.Config):

    @Bean
    def post_domain(self):
        return PostDomain()

    @Bean
    def post_repo(self):
        return PostRepo()

    @Bean
    def post_dao(self):
        return PostDaoSqlalchemy()

    @Bean
    def db_connection(self):
        rv = create_engine('sqlite:///test.db', echo=True)
        return rv

    @Bean
    def db_session_factory(self):
        engine = self.db_connection()
        rv = sessionmaker(engine)
        return rv
