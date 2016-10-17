# -*- coding: utf-8 -*-

class report_advertisement_current:

    __tablename__ = 'report_advertisement_current'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    advertisement_id = Column(INTEGER(11), nullable=False)

    report_date = Column(INTEGER(11), nullable=False)

    amount = Column(INTEGER(11), nullable=False)

    impression = Column(INTEGER(11), nullable=False)

    clicks = Column(INTEGER(11), nullable=False)

    effect_actions = Column(INTEGER(11), nullable=False)

    visitors = Column(INTEGER(11), nullable=False)

    click_visitors = Column(INTEGER(11), nullable=False)

    effect_visitors = Column(INTEGER(11), nullable=False)
