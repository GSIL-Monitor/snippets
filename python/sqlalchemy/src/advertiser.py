# -*- coding: utf-8 -*-

class advertiser:

    __tablename__ = 'advertiser'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    username = Column(VARCHAR(255), nullable=False)

    password_hash = Column(VARCHAR(255), nullable=False)

    password_salt = Column(VARCHAR(255), nullable=False)
