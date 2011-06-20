#!/usr/bin/env python
"""
Base view to be subclassed
"""

import pygtk
import gtk
import os

pygtk.require("2.0")

class GtkBaseView(object):
    """
    Main site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = ""

    def __init__(self, toplevel_name, control):
        """
        Basic view to be subclassed.
        """
        if not os.path.isfile(self.GLADE_FILE):
            raise RuntimeError("No glade file found.")

        self._control = control
        self._builder = gtk.Builder()
        self._builder.add_from_file(self.GLADE_FILE)
        self._toplevel_name = toplevel_name
        self._slaves = {}

    def __getitem__(self, name):
        """
        Returns widget named name
        """
        if self._builder.get_object(name) is not None:
            return self._builder.get_object(name)

        if self._slaves.has_key(name):
            return self._slaves[name]

        return None

    def get_toplevel(self):
        """
        Returns toplevel component
        """
        return self[self._toplevel_name]

    def get_toplevel_name(self):
        """
        Returns toplevel name component
        """
        return self._toplevel_name

    def attach_slave(self, name, container_name, slave):
        """
        Attach a slave view to the master view.
        """
        if not isinstance(slave, GtkBaseView):
            raise TypeError("slave must be a GtkBaseView, not a %s" %
                            type(slave))

        container = self._builder.get_object(container_name)

        if container is None:
            raise AttributeError("No container named %s" % name)

        slave_toplevel = slave.get_toplevel()
        widget = slave_toplevel.get_child()
        slave_toplevel.remove(widget)
        container.pack_end(widget)

        self._slaves[name] = slave

    def get_objects(self):
        """
        Returns all widgets
        """
        return self._builder.get_objects()

    def show(self):
        """
        Shows window
        """
        self.get_toplevel().show()
