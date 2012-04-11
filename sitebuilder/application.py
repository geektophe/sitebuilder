#!/usr/bin/env python
"""
This module contains application wide functions and settings
"""

#from signal import signal, SIGTERM
import sitebuilder.command.scheduler
import sitebuilder.command.log
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
    sitebuilder.command.scheduler.start()
    sitebuilder.command.log.start()


def uninit():
    """
    Leaves application
    """
    sitebuilder.command.scheduler.stop()
    sitebuilder.command.log.stop()
