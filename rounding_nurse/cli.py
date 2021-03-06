#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from logging import (DEBUG, getLogger, StreamHandler)
from time import sleep
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.parse import urljoin
import urllib.request

from bs4 import BeautifulSoup
from database.orm.models import Page
from database.orm.constant import State
from database.query import (
    find_page, find_previous_page, insert_page, update_state)

logger = getLogger(__name__)
handler = StreamHandler()
logger.setLevel(DEBUG)
logger.addHandler(handler)


def parse_response(response):
    soup = BeautifulSoup(response.read(), 'html.parser')
    for a in soup.find_all("a"):
        yield a


def get_next(response):

    for tag in parse_response(response):
        if not tag.has_attr('href'):
            continue
        try:
            href = tag['href']
            anchor_text = tag.get_text()
            target = urlparse(href)

            # in case of telephone nubmer
            if href.startswith("tel:") or href.startswith("#"):
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

    result_url = None
    sleep(interval)
    try:
        logger.debug("request to %s", url)
        response = urllib.request.urlopen(url)
        # consider redirect.
        result_url = response.geturl()
        logger.debug("insert page.")
        insert_page(result_url, url, response.code,
                    parent_id, txt, State.in_progress.value)
    except HTTPError as e:
        insert_page(result_url, url, e.code, parent_id,
                    txt, State.finished.value)
        return

    # find next crawl target and retry.
    new_parent = find_page(result_url)
    for l in get_next(response):
        do_request(
            Page(url=l.url, parent_id=new_parent.id, link_text=l.link_text))
    update_state(result_url, State.finished.value)


@click.command()
@click.option('-u', '--url', nargs=1, required=True, help='target root url.')
@click.option('-i', '--include', required=True, multiple=True, help='crawling enable domains.')
@click.option('-s', '--sleep_time', type=int, default=1, help='crawling interval: default is 1 second.')
def main(url, include, sleep_time):

    global allow_urls
    allow_urls = include
    global interval
    interval = sleep_time

    logger.debug("start crawling.")
    do_request(Page(url=url, parent_id=1, link_text=""))
    logger.debug("finish crawling.")

if __name__ == "__main__":

    main()
