# -*- coding: utf-8 -*-

class payment:

    __tablename__ = 'payment'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    advertiser_id = Column(INTEGER(11), nullable=False)

    amount = Column(INTEGER(11), nullable=False)

    amount_real = Column(INTEGER(11), nullable=False)

    discount = Column(INTEGER(11), nullable=False)

    create_time = Column(TIMESTAMP, nullable=False)

    update_time = Column(TIMESTAMP, nullable=False)

    status = Column(INTEGER(11), nullable=False)
