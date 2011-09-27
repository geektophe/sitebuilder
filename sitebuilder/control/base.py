#!/usr/bin/env python
"""
Base control Agent class to be subclassed
"""

from sitebuilder.observer.attribute import AttributeChangedObserver
from sitebuilder.observer.action  import ActionActivatedObserver


class BaseControlAgent(ActionActivatedObserver):
    """
    Base control Agent class to be subclassed
    """

    def __init__(self, read_only=False):
        """
        Initializes control agent.

        The read_only attribute indocates to the presentation that none of then
        widgets should be sensitive. The user is then not allowed to change any
        value.
        """

        self._read_only = read_only

    def get_read_only_flag(self):
        """
        Returns read only flag
        """
        return self._read_only

    def set_read_only_flag(self, read_only):
        """
        Returns read only flag
        """
        if not read_only is True and not read_only is False:
            raise TypeError("read only flag should be a boolean value")

        self._read_only = read_only

    def set_presentation_agent(self, presentation_agent):
        """
        Sets local PresentationAgent implementation instance
        """
        # TODO: perform better instance check on presentation agent
        if not isinstance(presentation_agent, AttributeChangedObserver):
            raise AttributeError("presentation agent should be an instance " +
                                 "of AttributeChangedObserver")

        self._presentation_agent = presentation_agent

    def get_presentation_agent(self):
        """
        Returns local PresentationAgent implementation instance
        """
        return self._presentation_agent

    def set_configuration(self, configuration):
        """
        Returns local PresentationAgent implementation instance
        """
        # TODO: perform instance check on configuration
        self._configuration = configuration

    def get_configuration(self):
        """
        Returns configuration instance
        """
        return self._configuration

    def get_attribute_value(self, name):
        """
        Returns a configuration attribute value
        """
        # TODO: check that presentation agent instance has been initialized
        return self._configuration.get_attribute(name).get_value()

    def set_attribute_value(self, name, value):
        """
        Returns a configuration attribute value
        """
        self._configuration.get_attribute(name).set_value(value)

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Destroyes presentation
        self.get_presentation_agent().destroy()
