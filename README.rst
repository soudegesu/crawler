============================
rounding-nurse
============================

`rounding-nurse` is a crawler that collects the HTTP Status of the web site.

.. class:: no-web no-pdf

|travis| |coverity| |climate| |coverage| |gemnasium|

Description
==============================

`rounding-nurse` searches the URL string of the href attribute of the <a> tag from the acquired page, and search the web page recursively.
There are examples of use cases as follows.

* Check dead links after web site renewal.


Usage
==============================

* install python modules

.. code-block:: sh

    pip install -r requirements.txt


* run rounding_nurse

.. code-block:: sh

    python rounding_nurse/crawl.py -u http://xxxx.xx.xx/ -i xxxx.xx.xx yyyy.yy.yy


.. |travis| image:: https://travis-ci.org/soudegesu/rounding_nurse.svg?branch=master
   :target: https://travis-ci.org/soudegesu/rounding_nurse
   :alt: Travis CI

.. |coverity| image:: https://scan.coverity.com/projects/11725/badge.svg
    :target: https://scan.coverity.com/projects/soudegesu-rounding_nurse
    :alt: Coverity Scan Build Status

.. |climate| image:: https://codeclimate.com/github/soudegesu/rounding_nurse/badges/gpa.svg
   :target: https://codeclimate.com/github/soudegesu/rounding_nurse
   :alt: Code Climate

.. |coverage| image:: https://coveralls.io/repos/github/soudegesu/rounding_nurse/badge.svg?branch=master
   :target: https://coveralls.io/github/soudegesu/rounding_nurse?branch=master
   :alt: Test Coverage

.. |gemnasium| image:: https://gemnasium.com/badges/github.com/soudegesu/rounding_nurse.svg
   :target: https://gemnasium.com/github.com/soudegesu/rounding_nurse
   :alt: Dependency Status
