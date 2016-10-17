# -*- coding: utf-8 -*-
import random

src = {
    'a': 6,
    'b': 3,
    'c': 1
}

r = []
for i in sorted(src.keys()):
    for j in range(src[i] * 10):
        r.append(i)

print(r)

result = {'a': 0, 'b': 0, 'c': 0}
for i in range(10000):
    result[random.choice(r)] += 1

print(result)
