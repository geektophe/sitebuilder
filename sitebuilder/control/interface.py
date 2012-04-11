#!/usr/bin/env python
"""
Control agent interface definition
"""

from zope.interface import Interface

class IControlAgent(Interface):
    """
    Control Agent interface
    """

    def is_read_only():
        """
        Returns component's read only state flag
        """

    def set_read_only(flag):
        """
        Sets component's read only state flag
        """

    def set_presentation_agent(presentation_agent):
        """
        Sets presentation agent instance
        """

    def get_presentation_agent():
        """
        Sets presentation agent instance
        """

    def set_configuration(configuration):
        """
        Sets configuration abstraction agent instance
        """

    def get_configuration():
        """
        Returns configuration abstraction agent instance
        """

    def get_attribute_value(name):
        """
        Returns abstraction agent's attribute value identified by name
        """

    def set_attribute_value(name, value):
        """
        Sets abstraction agent's attribute value identified by name
        """

    def destroy():
        """
        Cleanly destroyes all components
        """
