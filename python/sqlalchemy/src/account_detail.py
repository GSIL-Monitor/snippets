# -*- coding: utf-8 -*-

class account_detail:

    __tablename__ = 'account_detail'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    account_id = Column(INTEGER(11), nullable=False)

    balance = Column(INTEGER(11), nullable=False)

    amount = Column(INTEGER(11), nullable=False)

    amount_real = Column(INTEGER(11), nullable=False)

    note = Column(VARCHAR(255), nullable=False)

    create_time = Column(TIMESTAMP, nullable=False)

    type = Column(INTEGER(11), nullable=False)

    hash = Column(INTEGER(11), nullable=False)
