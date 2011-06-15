#!/usr/bin/env python
"""
This module contains several application parameters used in other modules.
"""

from os.path import abspath, basename

GLADE_BASEDIR = basename(abspath( __file__ )) + "../resources/glade"
