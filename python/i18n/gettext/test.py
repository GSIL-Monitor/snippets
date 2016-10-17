# -*- coding: utf-8 -*-
import gettext
import os


root = os.path.abspath(os.path.dirname(__file__))

gettext.bindtextdomain('test', root)
gettext.bind_textdomain_codeset('test', 'utf-8')
gettext.textdomain('test')

_ = gettext.gettext

print(_('invalid choice'))
