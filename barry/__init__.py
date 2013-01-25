#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
barry
=====
Barry is a Python library for automating assignment grading.

:copyright: (C) 2013, Matthew Frazier
:license:   MIT/X11, see LICENSE for details
"""
from .specs import Assignment, COMPLETE, PARTIAL, INCOMPLETE, EXTRA, SKIPPED
from .script import grading_session

