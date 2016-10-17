# -*- coding: utf-8 -*-
import random

src = [
    (20000, 8000),
    (7000, 15000),
    (1500, 10000),
    (300, 10000),
    (50, 10000),
    (0, 10000),
]

def left_level(input):
    if input == 0:
        return 0
    return round(input / 5000) + 1


def pending_level(input):
    if input == 0:
        return 0
    return round(input / 1000) + 1


choices = []
idx = 0
for i in src:
    a, b = left_level(i[0]), pending_level(i[1])
    print(i[0], i[1], a, b, a * b)

    for j in range(a * b):
        choices.append(idx)

    idx += 1


rv = {}
for i in range(100000):
    idx = random.choice(choices)
    if idx not in rv:
        rv[idx] = 0
    rv[idx] += 1

print(rv)
