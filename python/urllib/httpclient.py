# -*- coding: utf-8 -*-
import sys
import urllib.parse
from urllib.request import Request, build_opener

i = sys.version_info
v = '%d.%d.%d' % (i.major, i.minor, i.micro)

class HTTPResponse(object):

    def __init__(self):
        self.code = 0
        self.message = ''
        self.body = ''
        self.headers = {}

    @property
    def status_code(self):
        return self.code

    @property
    def reason(self):
        return self.message

class HTTPClient(object):

    def __init__(self):
        self.user_agent = 'Python %s HTTPClient' % v
        self.opener = build_opener()

        self.default_headers = {
            'User-Agent': self.user_agent
        }

    def http_request(self, url, method, data=None, headers={}):
        _headers = self.default_headers
        if data:
            if type(data) == dict:
                data = urllib.parse.urlencode(data).encode('ascii')
                _headers['Content-Type'] = 'application/x-www-form-urlencoded'
            elif hasattr(data, 'read'):
                data = data.read()
                _headers['Content-Type'] = 'application/binary'
            else:
                raise RuntimeError(
                    'unsupported data type: "%s"' % type(data))

            _headers.update(headers)

        req = Request(url, method=method, data=data, headers=_headers)
        resp = self.opener.open(req)
        rv = HTTPResponse()
        rv.code = resp.code
        rv.message = resp.reason
        rv.body = resp.read()
        for k in resp.headers.keys():
            rv.headers[k] = resp.headers[k]
        resp.close()
        return rv

    def get(self, url, params={}, headers={}):
        return self.http_request(url, 'GET', headers=headers)

    def post(self, url, data={}, headers={}):
        return self.http_request(url, 'POST', data=data, headers=headers)

    def put(self, url, data={}, headers={}):
        return self.http_request(url, 'PUT', data=data, headers=headers)

    def delete(self, url, data={}, headers={}):
        return self.http_request(url, 'DELETE', data=data, headers=headers)

default_http_client = HTTPClient()
def get(url, params={}, headers={}):
    return default_http_client.get(url, params, headers)

def post(url, data={}, headers={}):
    return default_http_client.post(url, data, headers)

def put(url, data={}, headers={}):
    return default_http_client.put(url, data, headers)

def delete(url, data={}, headers={}):
    return default_http_client.delete(url, data, headers)
