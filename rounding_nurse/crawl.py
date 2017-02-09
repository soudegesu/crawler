#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import chain
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.parse import urljoin
from time import sleep
import argparse
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative
from logging import getLogger, StreamHandler, DEBUG
from enum import IntEnum

global allow_urls
global interval

logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)
logger.addHandler(handler)


Base = sqlalchemy.ext.declarative.declarative_base()

class State(IntEnum):
    not_work = 0
    in_progress = 1
    finished = 2

class Page(Base):
    __tablename__ = 'page'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    url = sqlalchemy.Column(sqlalchemy.String(255))
    previous_url = sqlalchemy.Column(sqlalchemy.String(255))
    status = sqlalchemy.Column(sqlalchemy.Integer)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer)
    link_text = sqlalchemy.Column(sqlalchemy.Text)
    state = sqlalchemy.Column(sqlalchemy.Integer)

class SessionFactory(object):

    def __init__(self):
        self.engine = sqlalchemy.create_engine('mysql+pymysql://soudegesu:soudegesu@127.0.0.1/crawl?charset=utf8', echo=False)
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

    def __init__(self):
        self.session_factory = SessionFactory()

    def create(self):
        return SessionContext(self.session_factory.create())

def find_page(url):
    found_page = None
    with SessionContextFactory().create() as session:
        try:
            found_page = session.query(Page).filter_by(url=url).first()
        except Exception as e:
            logger.error("An error occurred while finding %s from database.", url, e)

    return found_page

def find_previous_page(previous_url):
    found_page = None
    with SessionContextFactory().create() as session:
        try:
            found_page = session.query(Page).filter_by(previous_url=previous_url).first()
        except Exception as e:
            logger.error("An error occurred while finding %s from database.", previous_url, e)

    return found_page

def insert_page(url, previous_url, status, parent_id, link_text, state):
    with SessionContextFactory().create() as session:
        try:
            logger.debug("insert data %s.", url)
            page = Page(url=url, previous_url=previous_url, status=status, parent_id=parent_id, link_text=link_text.strip(), state=state)
            session.add(page)
            session.commit()
        except Exception as e:
            logger.error("An error occurred while insert page data to database.", e)
            session.rollback()

def update_state(url, state):
    logger.info("%s:%s", url, state)
    with SessionContextFactory().create() as session:
        try:
            found_page = session.query(Page).filter_by(url=url).first()
            found_page.state = state
            session.commit()
        except Exception as e:
            logger.error("An error occurred while insert page data to database.", e)
            session.rollback()


def parse_response(response):
    soup = BeautifulSoup(response.read(), 'html.parser')
    for a in soup.find_all("a"):
        yield a

def get_next(response):
    
    for tag in parse_response(response):
        if not tag.has_attr('href'):
            continue
        try :
            href = tag['href']
            anchor_text = tag.get_text()
            target = urlparse(href)

            # in case of telephone nubmer
            if href.startswith("tel:")  or  href.startswith("#"):
                continue
            # skip javascript:void
            if target.scheme == 'javascript':
                continue

            new_link = Page(link_text=anchor_text)
            if target.scheme == 'http' and target.scheme == 'https':
                new_link.url = urlparse(href)
            else:
                new_link.url = urljoin(response.geturl(), href)
            yield new_link

        except Exception as e:
            logger.error("An error occurred while find anchor link.", e)
            continue

def do_request(p):

    url = p.url
    parent_id = p.parent_id
    txt = p.link_text

    # skip if url has already crawled.
    if urlparse(url).hostname not in allow_urls:
        logger.info("This domain is not target for crawling.(%s)", url)
        return

    if find_previous_page(url) is not None or find_page(url) is not None:
        logger.info("This url has been already crawled.(%s)", url)
        return

    response = None
    result_url = None
    sleep(interval)
    try:
        logger.debug("request to %s", url)
        response = urllib.request.urlopen(url)
        # consider redirect.
        result_url = response.geturl()
        logger.debug("insert page.")
        insert_page(result_url, url, response.code, parent_id, txt, State.in_progress.value)
    except HTTPError as e:
        insert_page(result_url, url, e.code, parent_id, txt, State.finished.value)
        return

    # find next crawl target and retry.
    new_parent = find_page(result_url)
    for l in get_next(response):
        do_request(Page(url=l.url, parent_id=new_parent.id, link_text=l.link_text))
    update_state(result_url, State.finished.value)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', nargs=1, required=True, help='target root url.')
    parser.add_argument('-i', '--include', nargs='+', action='append', required=True, help='crawling enable domains.')
    parser.add_argument('-s', '--sleep', nargs=1, type=int, default=1, help='crawling interval: default is 1 second.')
    args = parser.parse_args()

    #set global variables.
    allow_urls = list(chain.from_iterable(args.include))
    interval = args.sleep

    start = args.url[0]
    logger.debug("start crawling.")
    do_request(Page(url=start, parent_id=1, link_text=""))
    logger.debug("finish crawling.")
