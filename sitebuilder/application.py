#!/usr/bin/env python
"""
This module contains application wide functions and settings
"""

from threading import Event
from signal import signal, SIGTERM
import sys

threadstop = Event()


def init():
    """
    Setup application wide locks
    """
    pass

def uninit():
    """
    Leaves application
    """
    global threadstop
    threadstop.set()

def sig_stop(signum, frame):
    """
    Signal handler used to cleanly stop application on various signals
    """
    uninit()
    sys.exit()


# Registers signal handlers
#signal(SIGTERM, sig_stop)
