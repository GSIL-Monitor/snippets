# -*- coding: utf-8 -*-
import pprint
import sys

import sqlparse
from sqlparse.tokens import Token


if len(sys.argv) <= 1:
    print('{} <sql>'.format(sys.argv[0]))
    sys.exit()

sql = sys.argv[1]

sql = sqlparse.format(sql, reindent=True, keyword_case='upper')
print(sql)
