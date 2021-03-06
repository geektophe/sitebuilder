#!/usr/bin/env python
"""
Base view to be subclassed
"""

import pygtk
import gtk
import os
from sitebuilder.presentation.interface import IPresentationAgent
from sitebuilder.event.bus import EventBus
from zope.interface import implements

pygtk.require("2.0")

class GtkBasePresentationAgent(object):
    """
    Main site add/edit/view interface.

    The interface design is loaded from a glade file.
    """
    implements(IPresentationAgent)

    GLADE_FILE = ""
    TOPLEVEL_NAME = ""

    def __init__(self, control_agent):
        """
        Basic view to be subclassed.
        """
        if not os.path.isfile(self.GLADE_FILE):
            raise RuntimeError("No glade file found.")

        self._event_bus = EventBus()
        self._control_agent = control_agent
        self._builder = gtk.Builder()
        self._builder.add_from_file(self.GLADE_FILE)
        self._slaves = {}
        self._attr_validity = {}

    def __getitem__(self, name):
        """
        Returns widget named name
        """
        if self._builder.get_object(name) is not None:
            return self._builder.get_object(name)

        if self._slaves.has_key(name):
            return self._slaves[name]

        return None

    def get_event_bus(self):
        """
        Returns component's event bus.
        """
        return self._event_bus

    def get_control_agent(self):
        """
        Returns control agent instance
        """
        return self._control_agent

    def get_toplevel(self):
        """
        Returns toplevel component
        """
        return self[self.TOPLEVEL_NAME]

    def attach_slave(self, name, container_name, slave):
        """
        Attach a slave view to the master view.
        """
        if not isinstance(slave, GtkBasePresentationAgent):
            raise TypeError(
                "slave must be a GtkBasePresentationAgent, not a %s" % \
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

    def set_combobox_items(self, widget, items):
        """
        Sets an interface combobox items. Each item is composed of a mnemonic
        name and a label, but only the label is displayed in the combobox.
        """
        # The model is configured for rows composed of name and a label
        model = gtk.ListStore(str, str)
        widget.set_model(model)
        # A text rederer is used to display rows
        renderer = gtk.CellRendererText()
        widget.pack_start(renderer, True)
        # Only the row's label is displayed (second element of the tupple: 1)
        widget.add_attribute(renderer, 'text', 1)

        # Appends items to the combobox
        names = items.keys()
        names.sort()

        for name in names:
            model.append((name, items[name]))

        if names:
            widget.set_active(0)

    def set_list_items(self, widget, items):
        """
        Sets an interface combobox items. Each item is composed of a mnemonic
        name and a label, but only the label is displayed in the combobox.

        Items should be a list of tuples corresponding to tho number of items
        in the list moldel.
        """
        model = widget.get_model()
        model.clear()

        for item in items:
            model.append(item)

    def get_combobox_selection(self, widget):
        """
        Retrieves the value of the list selected item.
        """
        model = widget.get_model()
        index = widget.get_active()

        if index < 0:
            return None

        return model[index][0]

    def get_list_selection(self, widget):
        """
        Retrieves the value of the list selected item.
        """
        model, rows = widget.get_selection().get_selected_rows()
        return rows

    def set_list_selection(self, widget, value):
        """
        Selects the list row which name column equals value.
        """
        model = widget.get_model()
        index = 0

        for row in model:
            if row[0] == value:
                break
            index += 1

        if index < len(model):
            widget.set_active(index)
        else:
            widget.set_active(-1)

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Destroyes slaves if it has some
        for name, slave in self._slaves.items():
            slave.destroy()
            del self._slaves[name]

        # Clears event bus observers
        self.get_event_bus().unsubscribe_all()
        self.get_toplevel().destroy()

    def enable(self, name):
        """
        Enables a control (set it resopnsive to user actions)
        """
        self[name].set_sensitive(True)

    def disable(self, name):
        """
        Disables a control (set it unresopnsive to user actions)
        """
        self[name].set_sensitive(False)

    def set_enabled(self, name, state):
        """
        Enables or disables a control based on state value
        """
        self[name].set_sensitive(state)

    def set_items(self, name, items):
        """
        Sets a finite value selection control (ex. list or combo box)
        selectable items.
        """
        widget = self[name]

        if isinstance(widget, gtk.List) or isinstance(widget, gtk.TreeView):
            self.set_list_items(widget, items)
        elif isinstance(widget, gtk.ComboBox):
            self.set_combobox_items(widget, items)
        else:
            raise NotImplementedError('Unhandled control type for %s: %s' % \
                (name, widget.__class__.__name__))

    def get_value(self, name):
        """
        Reads a control value or state.
        """
        widget = self[name]

        if isinstance(widget, gtk.Entry):
            return widget.get_text()
        elif isinstance(widget, gtk.ToggleButton):
            return widget.get_active()
        elif isinstance(widget, gtk.ComboBox):
            return self.get_combobox_selection(widget)
        elif isinstance(widget, gtk.List) or isinstance(widget, gtk.TreeView):
            return self.get_list_selection(widget)
        else:
            raise NotImplementedError('Unhandled control type for %s: %s' % \
                (name, widget.__class__.__name__))

    def set_value(self, name, value):
        """
        Sets a control value or state.
        """
        widget = self[name]

        if isinstance(widget, gtk.Entry):
            widget.set_text(value)
        elif isinstance(widget, gtk.ToggleButton):
            widget.set_active(value)
        elif isinstance(widget, gtk.List) or isinstance(widget, gtk.ComboBox):
            self.set_list_selection(widget, value)
        else:
            raise NotImplementedError('Unhandled control type for %s: %s' % \
                (name, widget.__class__.__name__))

    def set_error(self, name, state, mesg=""):
        """
        Sets a crontrol in a state showing than an error occured or that all
        is correct.

        An optional error message to be displayed may be passed.
        """
        widget = self[name]

        if state:
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFCCCC'))
            widget.set_tooltip_text(mesg)
        else:
            widget.set_tooltip_text('')
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#90EE90'))
