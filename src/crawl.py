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
from sqlalchemy import text

global allow_urls
global interval

db_url = 'mysql+pymysql://soudegesu:soudegesu@127.0.0.1/crawl?charset=utf8'
result_set = set()

Base = sqlalchemy.ext.declarative.declarative_base()

class Page(Base):
    __tablename__ = 'page'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    url = sqlalchemy.Column(sqlalchemy.String(255))

class Link(Base):
    __tablename__ = 'link'
    
    url = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer)
    link_text = sqlalchemy.Column(sqlalchemy.Text)    

    
def find_page(url):
    # create session object
    engine = sqlalchemy.create_engine(db_url, echo=False)
    
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    try:
        found_page = session.query(Page).filter_by(url=url).first()
    except Exception as e:
        print(e)
    finally:
        session.close()

    return found_page

def insert_link(url, status, parent_id, link_text):
    engine = sqlalchemy.create_engine(db_url, echo=False)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    
    try:
        new_one = Link(url=url, status=status, parent_id=parent_id, link_text=link_text)
        session.add(new_one)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()


def insert_page(url):
    engine = sqlalchemy.create_engine(db_url, echo=False)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()

    try:
        page = Page(url=url)
        session.add(page)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
	    session.close()


# get all anchor tags
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
                
                new_link = Link(link_text=anchor_text) 
                if target.scheme == 'http' and target.scheme == 'https':
                    new_link.url = urlparse(href) 
                else:
                    new_link.url = urljoin(result_url, href)
                yield new_link

            except Exception as e:
                continue

def do_request(url, parent_id, txt):

        # skip if url has already crawled.         
        if urlparse(url).hostname not in allow_urls:
            return

        if find_page(url) is not None:
            return

        # change to already crawled. 
        response = None
        result_url = None
        sleep(interval)
        print('aaaaaa')
        try:
            response = urllib.request.urlopen(url)
            # consider redirect.
            result_url = response.geturl() 
            insert_page(result_url)
            insert_link(result_url, response.code, parent_id, txt)
        except HTTPError as e:
            insert_page(url)
            insert_link(url, e.code, parent_id, txt)
            return
        print('bbbbbb')

        # find next crawl target and retry.
        new_parent = find_page(result_url)
        (do_request(l.url, new_parent.id, l.txt) for l in get_next(response))


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
    do_request(start, 7, "")
