============================
rounding-nurse
============================

`rounding-nurse` is a crawler that collects the HTTP Status of the web site.

Description
==============================

`rounding-nurse` searches the URL string of the href attribute of the <a> tag from the acquired page, and search the web page recursively.
There are examples of use cases as follows.
* Check dead links after web site renewal.


Usage
==============================

* install python modules
`
pip install -r requirements.txt
`

* run rounding_nurse
`
python src/crawl.py -u http://xxxx.xx.xx/ -i xxxx.xx.xx yyyy.yy.yy
`


