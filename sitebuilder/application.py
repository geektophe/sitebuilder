#!/usr/bin/env python
"""
This module contains application wide functions and settings
"""

from threading import Event
from signal import signal, SIGTERM
import sys
import gobject

threadstop = Event()


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


def uninit():
    """
    Leaves application
    """
    global threadstop
    threadstop.set()
