# -*- coding: utf-8 -*-
import configparser

cp = configparser.ConfigParser()

cp.read('db.ini')

print(cp['qk_action']['user'])
