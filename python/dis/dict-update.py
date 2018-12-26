# -*- coding: utf-8 -*-
import dis

def update():
    d1 = {'one': 1}
    d1.update({'two': 2})

def literal():
    d1 = {'one': 1}
    d1['two'] = 2

dis.dis(update)
print('============')
dis.dis(literal)
