#!/usr/bin/env python
"""
This module contains application wide functions and settings
"""

from threading import Event


if 'threadstop' not in locals():
    # Threads should listen to this event to stop
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
