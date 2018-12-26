# -*- coding: utf-8 -*-
from sqlalchemy import Column, {{ import }}

# auto generated from {{ database }}.{{ tableName }}
# {{ time }}
class {{ tableName }}(Model):

    __tablename__ = '{{ tableName }}'

{{ columns }}
