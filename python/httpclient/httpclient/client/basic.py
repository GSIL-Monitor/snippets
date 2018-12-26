# -*- coding: utf-8 -*-
import logging
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests

from httpclient import consts
from .abstract import AbstractClient


logger = logging.getLogger()


class BasicHttpClient(AbstractClient):

    def __init__(self):
        self.session = requests.Session()

    def get(self, url, query=None, headers=None, **options):

        _url = self._get_url(url, query)
        logger.error('_url: {}'.format(_url))

        _headers = self._get_headers('get', headers)
        rv = self.session.get(_url, headers=_headers)
        return rv

    def post(self, url, query=None, params=None, headers=None, **options):
        raise NotImplementedError()

    def put(self, url, query=None, params=None, headers=None, **options):
        raise NotImplementedError()

    def _get_url(self, url, query):
        pr = urlparse(url)
        o_params = parse_qs(pr.query, keep_blank_values=True)
        o_params = {x: str(o_params[x][0]) for x in o_params}
        o_params.update(query)
        q = urlencode(o_params)
        logger.error('o_params: {}'.format(o_params))
        rv = urlunparse([
            pr.scheme, pr.netloc, pr.path, pr.params, q, pr.fragment])
        return rv

    def _get_headers(self, method, headers):
        headers = headers or {}
        rv = dict(headers)

        if method != 'get':
            if consts.HEADERS.CONTENT_TYPE not in headers:
                rv[consts.HEADERS.CONTENT_TYPE] = consts.CONTENT_TYPE.FORM

        if consts.HEADERS.UA not in headers:
            rv[consts.HEADERS.UA] = consts.DEFAULT.UA

        return rv
