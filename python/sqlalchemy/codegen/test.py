# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import pprint

logging.basicConfig(level=logging.CRITICAL)

import jinja2
from qianka.sqlalchemy import QKSQLAlchemy
from sqlalchemy import String, Integer, MetaData, TIMESTAMP
from sqlalchemy.ext.automap import automap_base

from util import config_from_pyfile


class GenRoutine(object):

    def __init__(self, table):
        self.table = table

        self.tableName = table.name
        self.columns = table.columns
        self.pk = table.primary_key
        self.constraints = table.constraints
        self.indexes = table.indexes

        self.imports = set()
        self.staged = {}

    def engage(self):
        columns = self.prepareColumns()
        self.staged['columns'] = columns
        self.preparePk(columns)

        self.staged['imports'] = set(self.imports)

        return self.staged

    def preparePk(self, columns):
        pkColumns = []
        for col in self.pk.columns:
            pkColumns.append(col.name)

        for k, col in columns.items():
            if k in pkColumns:
                col['options']['primary_key'] = True

    def prepareColumns(self):
        cols = {}
        for col in self.columns:
            definition = self._prepareSingleColumn(col)
            cols[col.name] = definition

        return cols

    def _prepareSingleColumn(self, col):
        colName = col.name
        definition = {
            'name': colName,
            'key': col.key,
            'columnType': self.getColumnType(col.type),
        }

        options = {}
        if col.nullable is False:
            options['nullable'] = False

        if isinstance(col.type, Integer) and col.autoincrement:
            options['autoincrement'] = True

        definition['options'] = options
        return definition

    def getColumnType(self, i):
        if isinstance(i, Integer):
            self.imports.add('Integer')
            rv = 'Integer'
        elif isinstance(i, String):
            self.imports.add('String')
            rv = 'String({})'.format(i.length)
        elif isinstance(i, TIMESTAMP):
            self.imports.add('TIMESTAMP')
            rv = 'TIMESTAMP'
        else:
            raise RuntimeError('not supported type: {}'.format(i))

        return rv


class SqlCodeGen(object):

    def __init__(self, config):
        self.config = config
        self.db = QKSQLAlchemy()
        self.db.configure(config)

        self.meta = {}
        self.base = {}

        self.templates = {}
        self._loadTemplates()

    def _loadTemplates(self):
        with open('column.tpl') as f:
            self.templates['column'] = jinja2.Template(f.read())

        with open('table.tpl') as f:
            self.templates['table'] = jinja2.Template(f.read())

    def reflect(self, tableName, bind):
        m = self.getMeta(bind)
        m.reflect(only=[tableName])
        base = self.getBase(bind, m)
        rv = base.classes.get(tableName)
        return rv

    def getMeta(self, bind):
        if bind in self.meta:
            return self.meta[bind]

        eng = self.db.get_engine(bind)
        m = MetaData(bind=eng)
        self.meta[bind] = m
        return m

    def getBase(self, bind, meta):
        if bind in self.base:
            return self.base[bind]
        base = automap_base(metadata=meta)
        base.prepare()
        self.base[bind] = base
        return base

    def autogen(self, tableName, bind='default'):
        model = self.reflect(tableName, bind)
        table = model.__table__

        # pprint.pprint(table.__dict__)

        staged = GenRoutine(table).engage()

        imports = staged['imports']
        tcol = self.templates['column']
        ttable = self.templates['table']

        columnContent = []
        for k, definition in staged['columns'].items():
            _ = ' ' * 4 + tcol.render(**definition)
            columnContent.append(_)
            # pprint.pprint(col.__dict__)
            # pprint.pprint(type(col.type))

        ctx = {
            'database': 'zhuanqian',
            'tableName': tableName,
            'columns': '\n'.join(columnContent),
            'import': ', '.join(sorted(imports)),
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        rv = ttable.render(**ctx)
        return rv


config = {}
config.update(config_from_pyfile('config.py'))


codegen = SqlCodeGen(config)
code = codegen.autogen('user_match')
print(code)
