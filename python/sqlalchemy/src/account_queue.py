# -*- coding: utf-8 -*-

class account_queue:

    __tablename__ = 'account_queue'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    account_id = Column(INTEGER(11), nullable=False)

    amount = Column(INTEGER(11), nullable=False)

    amount_real = Column(INTEGER(11), nullable=False)

    balance = Column(INTEGER(11), nullable=False)

    create_time = Column(TIMESTAMP, nullable=False)

    update_time = Column(TIMESTAMP, nullable=False)

    status = Column(INTEGER(11), nullable=False)

    type = Column(INTEGER(11), nullable=False)
