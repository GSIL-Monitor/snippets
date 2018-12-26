# -*- coding: utf-8 -*-
import copy
import dis

def copy_member():
    d1 = {'one': 1}
    d2 = d1.copy()

def constructor():
    d1 = {'one': 1}
    d2 = dict(d1)

def copy_module():
    d1 = {'one': 1}
    d2 = copy.copy(d1)


dis.dis(copy_member)
print('============')
dis.dis(constructor)
print('============')
dis.dis(copy_module)
