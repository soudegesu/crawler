#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from click.testing import CliRunner
from cli import main
import pytest


class TestCliOption():

    @pytest.mark.parametrize("options, expected",[
        ("-i hogehoge", 2), #url is required
        ("-u hogehoge", 2), # include is required
        ("-u hogehoge hughauga -i piyopiyo", 2), # url is required
        ("-u hogehoge -i piyopiyo -s aaa", 2), # sleep_time is integer
    ])
    def test_main_option_validate(self, options, expected):

        runner = CliRunner()
        result = runner.invoke(main, options)
        assert result.exit_code == expected
