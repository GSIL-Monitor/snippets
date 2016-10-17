# -*- coding: utf-8 -*-

class P(object):

    def __init__(self):
        pass


    def todo(self):
        print('----')
        print(issubclass(self.__class__, P))
        print(self.__class__ is P)

class C(P):
    pass

p = P()
p.todo()

c = C()
c.todo()
