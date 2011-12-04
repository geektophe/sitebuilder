#!/usr/bin/env python
"""
This module contains application wide functions and settings
"""

from signal import signal, SIGTERM
from sitebuilder.command.scheduler import start as sched_start
from sitebuilder.command.scheduler import stop as sched_stop
from sitebuilder.command.log import start as log_start
from sitebuilder.command.log import stop as log_stop
import sys
import gobject


def sig_stop(signum, frame):
    """
    Signal handler used to cleanly stop application on various signals
    """
    uninit()
    sys._exit()


def init():
    """
    Setup application wide locks
    """
    # Registers signal handlers
    #signal(SIGTERM, sig_stop)
    gobject.threads_init()
    sched_start()
    log_start()


def uninit():
    """
    Leaves application
    """
    sched_stop()
    log_stop()
