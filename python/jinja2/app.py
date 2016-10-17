# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

t = env.get_template('test.jinja2')

print(t.render(name='world'))
