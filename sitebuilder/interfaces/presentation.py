
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

    def load_widgets_data():
        """
        Updates presentation agent widgets based on configuraton settings
        """

    def destroy():
        """
        Cleanly destroyes component
        """
