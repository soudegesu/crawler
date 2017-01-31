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

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    url = sqlalchemy.Column(sqlalchemy.String(255))

class Link(Base):
    __tablename__ = 'link'
    
    url = sqlalchemy.Column(sqlalchemy.String(255), primary_key=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer)
    link_text = sqlalchemy.Column(sqlalchemy.Text)    

    
def is_exists(check_url):
    # create session object
    engine = sqlalchemy.create_engine(db_url, echo=False)
    
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    try:
        found_page = session.query(Page).filter_by(url=check_url).first()
    except Exception as e:
        print("select query is failed")
    finally:
        session.close()

    return found_page != None

def insert(url, status, parent_url, link_text):
    engine = sqlalchemy.create_engine(db_url, echo=False)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    session = Session()
    
    try:
        new_one = Page(url=url, status=status, parent_url=parent_url, link_text=link_text)   
        session.add(new_one)
        session.commit()
    except Exception as e:
        print("Insert failed.")
        session.rollback()
    finally:
        session.close()


# get all anchor tags
def parse_response(response):
        soup = BeautifulSoup(response.read(), 'html.parser')
        for a in soup.find_all("a"):
            yield a

def do_request(url, parent_url, txt):
        
        # skip if url has already crawled. 
        if is_exists(url):
            return
        
        request_target = urlparse(url)
        
        if request_target.hostname not in allow_urls:
            return

        response = None
        try:
            sleep(interval)
            response = urllib.request.urlopen(url)
            insert(url, response.code, parent_url, txt)
            print(url+":"+str(response.code))
        except HTTPError as e:
            # exclude 200
            insert(url, e.code, parent_url, txt)
            print(url+":"+str(e.code))            
            return
        #  condider redirecting
        result_url = response.geturl()
        result_set.add(result_url)
        
        for tag in parse_response(response):
            if not tag.has_attr('href'):
                continue
            try :            
                href = tag['href']
                anchor_text = tag.get_text()                
                target = urlparse(href)
                
                if href.startswith("tel:")  or  href.startswith("#"):
                    # in case of telephone nubmer
                    continue
                
                if target.scheme == 'javascript':
                    # skip javascript:void
                    continue
                elif target.scheme == 'http' and target.scheme == 'https':
                    target = urlparse(href)
                    do_request(target, result_url, anchor_text)
                else:
                    joined_url = urljoin(result_url, href)
                    do_request(joined_url, result_url, anchor_text)
            except Exception as e:
                continue

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', nargs=1, required=True, help='target root url.')
    parser.add_argument('-i', '--include', nargs='+', action='append', required=True, help='crawling enable domains.')
    parser.add_argument('-s', '--sleep', nargs=1, type=int, default=1, help='crawling interval: default is 1 second.')
    args = parser.parse_args()

    allow_urls = list(chain.from_iterable(args.include))
    interval = args.sleep
    
    do_request(args.url[0], "", "")
