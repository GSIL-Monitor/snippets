# -*- coding: utf-8 -*-
import argparse
import logging
import pprint

import flask

logging.basicConfig(level=logging.DEBUG)


webapp = flask.Flask(__name__)
webapp.debug = True


@webapp.route('/')
def index():
    return 'this is qk-ci'


@webapp.route('/qk-ci/gitlab-webhook')
def webhook():
    body = flask.request.data
    logging.debug('>>> new hook >>>')
    logging.debug(pprint.pformat(body))
    logging.debug('<<< hook end <<<')
    return 'ok'


ap = argparse.ArgumentParser()
ap.add_argument('-p', '--port', type=int, default=4399)

options = ap.parse_args()

webapp.run(port=options.port, host='0.0.0.0', threaded=True)
