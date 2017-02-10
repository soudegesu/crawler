#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlalchemy.orm
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()


class SessionFactory(object):

    def __init__(self, url):
        self.engine = sqlalchemy.create_engine(
            url, echo=False)
        Base.metadata.create_all(self.engine)

    def create(self):
        Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        return Session()


class SessionContext(object):

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class SessionContextFactory(object):

    def __init__(self, url):
        self.session_factory = SessionFactory(url)

    def create(self):
        return SessionContext(self.session_factory.create())
