
#!/usr/bin/env python
"""
Presentation agent interface definition
"""

from zope.interface import Interface

class IPresentationAgent(Interface):
    """
    Presentation agent interface definition
    """

    def get_control_agent():
        """
        Returns control agent instance
        """

    def attach_slave(name, container_name, slave):
        """
        Attach a sub (slave) presentation agent view
        """

    def show():
        """
        Shows window
        """

    def set_combobox_items(combobox, items):
        """
        Sets an interface combobox items. Each item is composed of a mnemonic
        name and a label, but only the label is displayed in the combobox.
        """

    def get_combobox_selection(combobox):
        """
        Retrieves the value of the combobox selected item.
        """

    def set_combobox_selection(combobox, value):
        """
        Selects the combobox row which name column equals value.
        """

    def set_entry_attribute(widget, attr_name):
        """
        Sets an entry widget text
        """

    def set_validity_flag(attr_name, flag):
        """
        When some widgets that require a validity check are set (typically,
        widgets that ask user to enter text, such as entries), the validity
        flag associated to it is saved.

        It may be used to forbid composite form submition if a sub component
        has an incorrect value set.
        """

    def is_valid():
        """
        Allows to know if the widgets composing a component are in a valid
        state.
        """

    def load_widgets_data():
        """
        Updates presentation agent widgets based on configuraton settings
        """

    def destroy():
        """
        Cleanly destroyes component
        """
