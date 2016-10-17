# -*- coding: utf-8 -*-

msgs = []

def flash(msg):
    msgs.append(msg)

def get_flash():

    yield msgs.pop(0)


flash('1')
flash('2')
flash('3')

print(get_flash())
