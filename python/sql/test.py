# -*- coding: utf-8 -*-
import pprint
import sys

import sqlparse
from sqlparse.tokens import Token


sql = """SELECT a.id, a.keyword FROM appstore_keyword a
        LEFT OUTER JOIN keyword b
        ON a.id = b.keyword_id
        WHERE (b.priority = 0 OR b.id is NULL) AND a.is_skip = 0
        AND a.id > :offset ORDER BY a.id
        LIMIT 2, 10"""

if len(sys.argv) > 1:
    sql = sys.argv[1]

print('=======')
print('raw: \n{}'.format(sql))
print('=======')

sql = sqlparse.format(sql, reindent=True, keyword_case='upper')

print('formatted: \n{}'.format(sql))
print('=======')

stmts = sqlparse.parse(sql)
print(len(stmts))

token_group = {}
print(stmts[0].tokens)

print('=======')
print('restored: \n{}'.format(sqlparse.format(str(stmts[0]))))
print('=======')

ddl = False
dml = []
write = False
limit = None

for token in stmts[0].tokens:
    print(token.__class__, token.ttype, token.value)
    # print(type(token.ttype))
    if token.ttype == Token.Keyword.DDL:
        ddl = True
    if token.ttype == Token.Keyword.DML:
        dml.append(token.value)

for _ in dml:
    if _ != 'SELECT':
        write = True

# 单独找出LIMIT
idx = -1
l = len(stmts[0].tokens)
for i, token in zip(range(l), stmts[0].tokens):
    if token.ttype == Token.Keyword:
        if token.value.upper() == 'LIMIT':
            idx = i
            break

# pprint.pprint(idx)

if idx != -1:
    # 找到 LIMIT，一般格式化后的LIMIT参数总是在隔开一个空白字符后
    # 即中间有一个 Token.Text.Whitespace (这个无所谓，不用来判断)
    if l - idx >= 2:
        # 确保LIMIT后面至少有2个token
        pprint.pprint('ttype: %s' % token.ttype)
        token = stmts[0].tokens[idx+2]
        if token.ttype == Token.Literal.Number.Integer:
            # 单个数字
            limit = {
                'limit': int(token.value),
                'offset': None
            }
        if isinstance(token, sqlparse.sql.IdentifierList):
            # 多个参数
            integerCnt = 0
            intTokens = []
            for subtoken in token.tokens:
                if subtoken.ttype == Token.Literal.Number.Integer:
                    integerCnt += 1
                    intTokens.append(subtoken)
            if integerCnt == 2:
                # 只能是2个参数
                offset = int(intTokens[0].value)
                _limit = int(intTokens[1].value)
                limit = {
                    'limit': _limit,
                    'offset': offset,
                }

rating = {
    'ddl': ddl,
    'dml': dml,
    'write': write,
    'limit': limit,
}

print('rating: \n{}'.format(pprint.pformat(rating)))
