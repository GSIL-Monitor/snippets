# -*- coding: utf-8 -*-

class profile:

    __tablename__ = 'profile'


    id = Column(INTEGER(11), primary_key=True, nullable=False)

    display_name = Column(VARCHAR(255), nullable=False)
