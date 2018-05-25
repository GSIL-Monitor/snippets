# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import (
    Table, Column, Integer, MetaData, String, create_engine,
)
from sqlalchemy.orm import mapper, sessionmaker

en = create_engine('mysql+mysqldb://root@127.0.0.1/test?charset=utf8')
# 创建表的时候需要用到meta对象，用于绑定到某个数据库引擎里
# 便于操作meta信息
meta = MetaData(bind=en)


class UserLog(object):

    mapper = {}

    @staticmethod
    def getTable(date):
        """
        根据时间获取动态的ORM对象
        """
        # 先拿到动态的表名与类名
        tableName = date.strftime('user_log_%Y%m%d')
        clsName = date.strftime('UserLog%Y%m%d')

        # 缓存，不需要重复创建
        if clsName in UserLog.mapper:
            return UserLog.mapper[clsName]

        # 定义一个新的映射对象
        table = Table(
            tableName, meta,

            # 这里 key 参数作用是作为对象的属性使用
            # 例如 userLog.rowId
            Column(
                'id', Integer, autoincrement=True, primary_key=True,
                key='rowId'),
            Column('name', String(255), default=''),
        )
        # 动态定义一个类，三个参数含义分别为
        # - 类名
        # - 从哪里继承
        # - 定义成员内容
        cls = type(clsName, (UserLog,), {})

        # sqlalchemy，将类映射到表
        mapper(cls, table)
        UserLog.mapper[clsName] = cls
        return cls


ss = sessionmaker(bind=en)
s = ss()

dt = datetime.now()
# 根据参数动态获取ORM对象
model = UserLog.getTable(dt)
# 接下来用法和正常的保持一致
s.query(model).all()
