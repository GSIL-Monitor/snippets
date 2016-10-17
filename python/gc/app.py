# -*- coding: utf-8 -*-

import gc

s = {}
for i in gc.get_objects():
    _ = str(type(i))
    if _ in s:
        s[_] += 1
    else:
        s[_] = 1

def filter(_):
    k, v = _
    if v > 100:
        return (k, v)

for item in map(filter, s.items()):
    if item:
        print(item[0], item[1])

class A(object):

    _hello = None

    @property
    def hello(self):
        if self._hello is None:
            self._hello = 1
        return self._hello

    # @hello.setter
    # def hello(self, value):
    #     setattr(self, '_hello', value)

    @hello.deleter
    def hello(self):
        self._hello = None


a = A()

print(a.hello)
# a.hello = 1
del a.hello
# print(a.hello)
