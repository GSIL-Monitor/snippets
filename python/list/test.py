# -*- coding: utf-8 -*-

listA = [1, 2, 5, 7, 8, 10]
listB = [10, 2, 6, 7]

ra = [i for i in listA if i in listB]
rb = [i for i in listB if i in listA]

print(ra)
print(rb)

_c = 0
indexA = {}
for i in listA:
    indexA[i] = _c

_c = 0
indexB = {}
for i in listB:
    indexB[i] = _c

inter = set(listA).intersection(set(listB))

print(inter)
