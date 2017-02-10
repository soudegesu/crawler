#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .con.session import SessionContextFactory
from .models import Page
from logging import (DEBUG, getLogger, StreamHandler)

import os
import configparser

config = configparser.ConfigParser()
config.sections()
config.read(os.path.join(os.path.dirname(__file__), 'connection.conf'))
db_url = config["mysql"]["url"]


logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)


def find_page(url):
    found_page = None
    with SessionContextFactory(db_url).create() as session:
        try:
            found_page = session.query(Page).filter_by(url=url).first()
        except Exception as e:
            logger.error(
                "An error occurred while finding %s from database.", url, e)

    return found_page


def find_previous_page(previous_url):
    found_page = None
    with SessionContextFactory(db_url).create() as session:
        try:
            found_page = session.query(Page).filter_by(
                previous_url=previous_url).first()
        except Exception as e:
            logger.error(
                "An error occurred while finding %s from database.", previous_url, e)

    return found_page


def insert_page(url, previous_url, status, parent_id, link_text, state):
    with SessionContextFactory(db_url).create() as session:
        try:
            logger.debug("insert data %s.", url)
            page = Page(url=url, previous_url=previous_url,
                        status=status, parent_id=parent_id,
                        link_text=link_text.strip(), state=state)
            session.add(page)
            session.commit()
        except Exception as e:
            logger.error(
                "An error occurred while insert page data to database.", e)
            session.rollback()


def update_state(url, state):
    logger.info("%s:%s", url, state)
    with SessionContextFactory(db_url).create() as session:
        try:
            found_page = session.query(Page).filter_by(url=url).first()
            found_page.state = state
            session.commit()
        except Exception as e:
            logger.error(
                "An error occurred while insert page data to database.", e)
            session.rollback()
