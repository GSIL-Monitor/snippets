# -*- coding: utf-8 -*-
from frozendict import frozendict

a = {
    1: '2',
    2: '3',
}

f = frozendict(a)
f.update(a='4')
