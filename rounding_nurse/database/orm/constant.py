#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum


class State(IntEnum):
    not_work = 0
    in_progress = 1
    finished = 2
