# -*- coding: utf-8 -*-

class report_advertiser_daily:

    __tablename__ = 'report_advertiser_daily'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    advertiser_id = Column(INTEGER(11), nullable=False)

    report_date = Column(INTEGER(11), nullable=False)

    amount = Column(INTEGER(11), nullable=False)

    impression = Column(INTEGER(11), nullable=False)

    clicks = Column(INTEGER(11), nullable=False)

    effect_actions = Column(INTEGER(11), nullable=False)

    visitors = Column(INTEGER(11), nullable=False)

    click_visitors = Column(INTEGER(11), nullable=False)

    effect_visitors = Column(INTEGER(11), nullable=False)
