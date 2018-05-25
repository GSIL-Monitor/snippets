# -*- coding: utf-8 -*-
import logging
from flask import Flask, request

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route('/a/3.0/app.report', methods=['GET', 'POST'])
def report():
    v = request.values
    data = request.data
    logger.error('values: {}'.format(v))
    logger.error('data: {}'.format(data))
    return ''


app.run('0.0.0.0', port=3000, threaded=True)
