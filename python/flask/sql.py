# -*- coding: utf-8 -*-
import logging
import warnings

import flask
from flask import _request_ctx_stack
import flask_sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
connection_stack = _request_ctx_stack

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

class SessionHolder(object):

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self._sessions = {}

        @app.teardown_appcontext
        def shutdown_session(response_or_exc):
            keys = [x for x in self._sessions.keys()]
            for k in keys:
                s = self._sessions.pop(k)
                if s:
                    logger.debug(
                        'shutdown_session: dispose session %s' % k)
                    s.remove()
            return response_or_exc

    def __call__(self, name='default'):
        if name in self._sessions:
            return self._sessions.get(name)

        engine = self.db.get_engine(self.app, name)
        session = sessionmaker(bind=engine)
        s = scoped_session(
            session, scopefunc=connection_stack.__ident_func__)
        self._sessions[name] = s
        return s

    def __getattr__(self, name):
        session = self()
        return getattr(session, name)

webapp = flask.Flask('sql')
webapp.debug = True

webapp.config['SQLALCHEMY_DATABASE_URI'] \
    = 'mysql+pymysql://dbaroot@172.16.3.234/ops'

webapp.config['SQLALCHEMY_BINDS'] = {
    'default': 'mysql+pymysql://dbaroot@172.16.3.234/ops',
    'local': 'mysql+pymysql://root@127.0.0.1/ops',
}

db = flask_sqlalchemy.SQLAlchemy(webapp)
db.session = SessionHolder(webapp, db)

def index():
    row = db.session.execute('show variables like "version"').fetchone()
    print(row)
    row = db.session('local').execute(
        'show variables like "version"').fetchone()
    print(row)
    return ''

webapp.route('/')(index)

webapp.run('0.0.0.0', port=3000, threaded=True)
