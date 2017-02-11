#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Connect to the database using SQLAlchemy.
To use the module, please write as fellows.

SessionContextFactory.create(db_url).create()
"""

import sqlalchemy.orm
import sqlalchemy

Base = sqlalchemy.ext.declarative.declarative_base()


class SessionFactory(object):
    """
    Session Maker wrapper.
    """

    def __init__(self, url):
        self.engine = sqlalchemy.create_engine(
            url, echo=False)
        Base.metadata.create_all(self.engine)

    def create(self):
        Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        return Session()


class SessionContext(object):
    """
    Make it possible to close with `with` statement.
    """

    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class SessionContextFactory(object):
    """
    create SessionContext
    """
    @staticmethod
    def create(url):
        return SessionContext(SessionFactory(url).create())
