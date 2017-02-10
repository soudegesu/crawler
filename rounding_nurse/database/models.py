#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()


class Page(Base):
    __tablename__ = 'page'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    url = sqlalchemy.Column(sqlalchemy.String(255))
    previous_url = sqlalchemy.Column(sqlalchemy.String(255))
    status = sqlalchemy.Column(sqlalchemy.Integer)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer)
    link_text = sqlalchemy.Column(sqlalchemy.Text)
    state = sqlalchemy.Column(sqlalchemy.Integer)