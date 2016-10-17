# -*- coding: utf-8 -*-

class account:

    __tablename__ = 'account'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    balance = Column(INTEGER(11), nullable=False)

    queue_id = Column(INTEGER(11), nullable=False)

    create_time = Column(TIMESTAMP, nullable=False)

    update_time = Column(TIMESTAMP, nullable=False)

    status = Column(INTEGER(11))
