from distutils.core import (setup, Command)
from setuptools import setup, find_packages
import sys
sys.path.append('./rounding_nurse')
sys.path.append('./tests')


# class PyTest(Command):
#     user_options = []
#
#     def initialize_options(self):
#         pass
#
#     def finalize_options(self):
#         pass
#
#     def run(self):
#         import pytest
#         pytest.main()


setup(
    name = "rounding_nurse",
    version = "0.0.1",
    author = "soudegesu",
    packages = find_packages(),
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    test_suite = ['test']
    # cmdclass={'test', PyTest}
)