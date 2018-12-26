# -*- coding: utf-8 -*-


class AbstractClient(object):

    def get(self, url, query, headers, **options):
        raise NotImplementedError()

    def post(self, url, query, params, headers, **options):
        raise NotImplementedError()

    def put(self, url, query, params, headers, **options):
        raise NotImplementedError()

    def _parse_url(self, url):
        pass

    def _regularize_url(self, url, query):
        pass
