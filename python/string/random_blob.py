# -*- coding: utf-8 -*-
import random
import string
import sys

l = lambda: random.choice(string.ascii_letters)

size = 32
if len(sys.argv) > 1:
    size = int(sys.argv[1])

o = ''.join(l() for x in range(size))
print(o)
