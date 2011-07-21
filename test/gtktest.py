#!/usr/bin/env python
"""
Functions helpful to test PyGTK applications
"""

import time
import gtk

# Stolen from Kiwi
def refresh_gui(delay=0):
    """
    Emulates GTK applicaiton main loop event handler in synchronous way
    """
    while gtk.events_pending():
        gtk.main_iteration_do(block=False)

    time.sleep(delay)
