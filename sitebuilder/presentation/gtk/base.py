#!/usr/bin/env python
"""
Base view to be subclassed
"""

import pygtk
import gtk
import gtk.glade
import os

pygtk.require("2.0")

class GtkBasePresentation(object):
    """
    Main site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = ""

    def __init__(self, control):
        """
        Basic view to be subclassed.
        """
        if not os.path.isfile(self.GLADE_FILE):
            raise RuntimeError("No glade file found.")

        self._control = control
        self._widgets = gtk.glade.XML(self.GLADE_FILE)

    def __getitem__(self, name):
        """
        Returns widget named name
        """
        return self._widgets.get_widget(name)
