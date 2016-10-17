# -*- coding: utf-8 -*-

class report_summary_current:

    __tablename__ = 'report_summary_current'


    advertiser_id = Column(INTEGER(11), primary_key=True, nullable=False)

    amount_00 = Column(INTEGER(11), nullable=False)

    amount_01 = Column(INTEGER(11), nullable=False)

    amount_07 = Column(INTEGER(11), nullable=False)

    amount_30 = Column(INTEGER(11), nullable=False)

    balance = Column(INTEGER(11), nullable=False)

    update_time = Column(TIMESTAMP, nullable=False)
