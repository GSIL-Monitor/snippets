# -*- coding: utf-8 -*-
import simplejson as json
import argparse

from ploceus.api import task, run, run_task


def task_result_serializable(o):
    rv = {}
    rv['rv'] = o.rv
    rv['name'] = o.name
    rv['error'] = o.error
    rv['ok'] = o.ok
    rv['failed'] = o.failed
    return rv


@task
def test():
    run('date')
    run('sp', _raise=False)
    return 'hello'


ap = argparse.ArgumentParser()
ap.add_argument('--hostname', default=[], action='append')
ap.add_argument('--task', required=True)

options = ap.parse_args()

if options.task in locals():
    task = locals()[options.task]

result = {}
rv = run_task(task, options.hostname)
for i in rv.items():
    k, v = i
    result[k] = task_result_serializable(v)

print('--------PLOCEUS RUBY RESULT START--------')
print(json.dumps(result))
print('')
print('--------PLOCEUS RUBY RESULT END--------')
