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

    def get_toplevel():
        """
        Returns toplevel component
        """

    def attach_slave(name, container_name, slave):
        """
        Attach a sub (slave) presentation agent view
        """

    def show():
        """
        Shows window
        """

    def destroy():
        """
        Cleanly destroyes component
        """

    def enable(name):
        """
        Enables a control (set it resopnsive to user actions)
        """

    def disable(name):
        """
        Disables a control (set it inresopnsive to user actions)
        """

    def set_enabled(name, state):
        """
        Enables or disables a control based on state value
        """

    def get_value(name):
        """
        Reads a control value or state.
        """

    def set_value(name, value):
        """
        Sets a control value or state.
        """

    def set_isems(name, items):
        """
        Sets a finite value selection control (ex. list or combo box)
        selectable items.
        """

    def set_error(name, state, mesg=""):
        """
        Sets a crontrol in a state showing than an error occured or that all
        is correct.

        An optional error message to be displayed may be passed.
        """
