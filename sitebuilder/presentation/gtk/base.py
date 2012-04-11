#!/usr/bin/env python
"""
Base view to be subclassed
"""

import pygtk
import gtk
import os
from sitebuilder.observer.validity import IValidityObserver, ValiditySubject
from sitebuilder.observer.validity import ValidityChangedEvent
from sitebuilder.observer.attribute import IAttributeObserver
from sitebuilder.presentation.interface import IPresentationAgent
from sitebuilder.observer.action import ActionSubject
from sitebuilder.exception import FieldFormatError
from zope.interface import implements
from zope.schema import ValidationError

pygtk.require("2.0")

class GtkBasePresentationAgent(ValiditySubject, ActionSubject):
    """
    Main site add/edit/view interface.

    The interface design is loaded from a glade file.
    """
    implements(IValidityObserver, IAttributeObserver, IPresentationAgent)

    GLADE_FILE = ""
    TOPLEVEL_NAME = ""

    def __init__(self, control_agent):
        """
        Basic view to be subclassed.
        """
        if not os.path.isfile(self.GLADE_FILE):
            raise RuntimeError("No glade file found.")

        ValiditySubject.__init__(self)
        ActionSubject.__init__(self)
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
        # When a slave is attached, the master should be informed of its
        # validity changes
        slave.register_validity_observer(self)
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

    def set_combobox_attribute(self, widget, attr_name):
        """
        Retrieves an entry widget text, and tries to set it in the model.

        If an AttributeError is risen while setting the attribute (indicating
        an incorrect value), the widget backgroud is set red and a tooltip
        indicates the error.
        """
        value = self.get_combobox_selection(widget)

        try:
            self.get_control_agent().set_attribute_value(attr_name, value)
            widget.set_tooltip_text('')
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#90EE90'))
            self.set_validity_flag(attr_name, True)
        except (ValidationError, FieldFormatError), e:
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFCCCC'))
            widget.set_tooltip_text(str(e))
            self.set_validity_flag(attr_name, False)

    def set_entry_attribute(self, widget, attr_name, empty_allowed=True):
        """
        Retrieves an entry widget text, and tries to set it in the model.

        If an AttributeError is risen while setting the attribute (indicating
        an incorrect value), the widget backgroud is set red and a tooltip
        indicates the error.
        """
        value = widget.get_text()

        try:
            if not empty_allowed and not value:
                raise FieldFormatError('Required value')

            self.get_control_agent().set_attribute_value(attr_name, value)
            widget.set_tooltip_text('')
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#90EE90'))
            self.set_validity_flag(attr_name, True)
        except (ValidationError, FieldFormatError), e:
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFCCCC'))
            widget.set_tooltip_text(str(e))
            self.set_validity_flag(attr_name, False)

    def validity_changed(self, state):
        """
        ValidityChangedObserver trigger mmethod local implementation

        Default behaviour is to forwards ValidityChangedEvent to other
        components such as upper level presentation agents.
        """
        self.notify_validity_changed(state)

    def set_validity_flag(self, attr_name, flag):
        """
        When some widgets that require a validity check are set (typically,
        widgets that ask user to enter text, such as entries), the validity
        flag associated to it is saved.

        It may be used to forbid composite form submition if a sub component
        has an incorrect value set.
        """
        self._attr_validity[attr_name] = flag
        self.notify_validity_changed(ValidityChangedEvent(flag, id(self)))

    def get_validity_flag(self):
        """
        Allows to know if the widgets composing a component are in a valid
        state.
        """
        flag = True

        for attr_validity in self._attr_validity.values():
            flag = flag and attr_validity

        return flag

    def attribute_changed(self, attribute=None):
        """
        AttributeChangedObserver trigger mmethod local implementation
        """
        self.load_widgets_data()

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Destroyes slaves if it has some
        for name, slave in self._slaves.items():
            slave.remove_validity_observer(self)
            slave.destroy()
            del self._slaves[name]

        # Clears observers lists
        self.clear_validity_observers()
        self.clear_action_observers()
        self.get_toplevel().destroy()
