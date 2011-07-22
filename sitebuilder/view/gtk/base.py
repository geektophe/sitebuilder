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

    def __init__(self, toplevel_name, controller):
        """
        Basic view to be subclassed.
        """
        if not os.path.isfile(self.GLADE_FILE):
            raise RuntimeError("No glade file found.")

        self._controller = controller
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
            raise AttributeError("No container named %s" % container_name)

        slave_toplevel = slave.get_toplevel()
        widget = slave_toplevel.get_child()
        slave_toplevel.remove(widget)
        container.pack_start(widget)
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

    def set_combobox_items(self, combobox, items):
        """
        Sets an interface combobox items. Each item is composed of a mnemonic
        name and a label, but only the label is displayed in the combobox.
        """
        # The model is configured for rows composed of name and a label
        model = gtk.ListStore(str, str)
        combobox.set_model(model)
        # A text rederer is used to display rows
        renderer = gtk.CellRendererText()
        combobox.pack_start(renderer, True)
        # Only the row's label is displayed (second element of the tupple: 1)
        combobox.add_attribute(renderer, 'text', 1)

        # Appends items to the combobox
        names = items.keys()
        names.sort()

        for name in names:
            model.append((name, items[name]))

    def get_combobox_selection(self, combobox):
        """
        Retrieves the value of the combobox selected item.
        """
        model = combobox.get_model()
        index = combobox.get_active()

        if index < 0:
            return None

        return model[index][0]

    def set_combobox_selection(self, combobox, value):
        """
        Selects the combobox row which name column equals value.
        """
        model = combobox.get_model()
        index = 0

        for row in model:
            if row[0] == value:
                break
            index += 1

        if index < len(model):
            combobox.set_active(index)
        else:
            combobox.set_active(-1)

    def set_entry_attribute(self, widget, attribute):
        """
        Retrieves an entry widget text, and tries to set it in the model.

        If an AttributeError is risen while setting the attribute (indicating
        an incorrect value), the widget backgroud is set red and a tooltip
        indicates the error.
        """
        value = widget.get_text()

        try:
            self._controller.set_attribute_value(attribute, value)
            widget.set_tooltip_text('')
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#90EE90'))
        except AttributeError, e:
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFCCCC'))
            widget.set_tooltip_text(str(e))

