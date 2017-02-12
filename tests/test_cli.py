#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cli import main

import pytest


class TestCli():

    def test_main_argument_error(self):

        main()

# if __name__ == "__main__":
#     pytest.main()