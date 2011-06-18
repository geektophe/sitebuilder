#!/usr/bin/env python
"""
Base view to be subclassed
"""

import pygtk
import gtk
import os

pygtk.require("2.0")

class GtkBasePresentation(object):
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

        for slave in self._slaves:
            if self[name] is not None:
                return slave[name]

        return None

    def items(self):
        """
        Returns th elist of contained widgets
        """
        return self._builder.get_objects()

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

    def attach_slave(self, name, slave):
        """
        Attach a slave window content as a composite component.

        Attaches a slaveview to the current view, substituting the
        widget specified by name.  the widget specified *must* be a
        eventbox; its child widget will be removed and substituted for
        the specified slaveview's toplevel widget::

         .-----------------------. the widget that is indicated in the diagram
         |window/view (self.view)| as placeholder will be substituted for the
         |  .----------------.   | slaveview's toplevel.
         |  | eventbox (name)|   |  .-----------------.
         |  |.--------------.|      |slaveview (slave)|
         |  || placeholder  <----.  |.---------------.|
         |  |'--------------'|    \___ toplevel      ||
         |  '----------------'   |  ''---------------'|
         '-----------------------'  '-----------------'

        the original way of attachment (naming the *child* widget
        instead of the eventbox) is still supported for compatibility
        reasons but will print a warning.
        """
        if not isinstance(slave, GtkBasePresentation):
            raise TypeError("slave must be a GtkBasePresentation, not a %s" %
                            type(slave))

        self._slaves[name] = slave
        slave_toplevel = slave.get_toplevel()

        slave_toplevel = slave.get_toplevel()

        if isinstance(slave_toplevel, gtk.Window): # view with toplevel window
            new_widget = slave_toplevel.get_child()
            slave_toplevel.remove(new_widget) # remove from window to allow reparent
        else: # slaveview
            new_widget = slave_toplevel

        placeholder = self.get_widget(name)

        if not placeholder:
            raise AttributeError(
                  "slave container widget `%s' not found" % name)
        parent = placeholder.get_parent()

