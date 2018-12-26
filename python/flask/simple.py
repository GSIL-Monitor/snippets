# -*- coding: utf-8 -*-
from functools import wraps
import logging
from datetime import datetime, timedelta

from flask import Blueprint, Flask, request, render_template, make_response
from flask import session


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10
app.config['SECRET_KEY'] = 'hello'
app.debug = True
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    expiration = datetime.now() + timedelta(days=1)
    resp = _index()
    resp.set_cookie('hello', '1', expires=expiration)
    return resp


def _index():
    resp = make_response(render_template('index.html'))
    resp.cache_control.public = True
    resp.cache_control.max_age = 300
    resp.headers['Etag'] = '"v1"'
    extra = timedelta(seconds=300)
    lm = resp.last_modified or datetime.now()
    resp.expires = lm + extra
    return resp.make_conditional(request)


@app.route('/index.html')
def index_html():
    return _index()


class MyBlueprint(Blueprint):

    def route(self, rule, **options):
        logger.error('rule: {}'.format(rule))

        def decorator(f):
            logger.error('f: {}'.format(f))
            endpoint = options.pop("endpoint", f.__name__)
            endpoint = rule
            logger.error('MyBlueprint.decorator')
            logger.error('endpoint: {}'.format(endpoint))

            @wraps(f)
            def wrapper(*args, **kwargs):
                logger.error('wrapper')
                from flask import redirect
                return redirect('/2')
                return f(*args, **kwargs)
            self.add_url_rule(rule, endpoint, wrapper, **options)
            return wrapper
        return decorator


demo = MyBlueprint('demo', 'demo')


@demo.route('/1')
@demo.route('/2')
def demo_index():
    logger.error('demo_index controller')
    return ''


app.register_blueprint(demo, url_prefix='/demo')
app.run('0.0.0.0', port=3000, threaded=True)
