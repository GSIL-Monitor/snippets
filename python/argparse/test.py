# -*- coding: utf-8 -*-

import argparse



ap = argparse.ArgumentParser()


subparsers = ap.add_subparsers()

parser_task = subparsers.add_parser('task')

parser_task.add_argument('--id', required=True)


parser_adv = subparsers.add_parser('adv')

parser_adv.add_argument('--id', required=True)


options = ap.parse_args()

print(options)
print('id' in options)
