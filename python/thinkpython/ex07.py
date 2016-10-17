# -*- coding: utf-8 -*-

class Kangaroo(object):

    def __init__(self):
        self.pouch_contents = list()

    def put_in_pouch(self, item):
        self.pouch_contents.append(item)

    def __repr__(self):
        return "<Kangaroo %s>" % str(self.pouch_contents)


kanga = Kangaroo()
roo = Kangaroo()
kanga.put_in_pouch(roo)

print(kanga)
print(roo)
