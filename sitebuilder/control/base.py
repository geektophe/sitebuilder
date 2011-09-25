#!/usr/bin/env python
"""
Base control Agent class to be subclassed
"""

from sitebuilder.observer.attribute import AttributeChangedObserver
from sitebuilder.observer.validity  import ValidityChangedObserver
from sitebuilder.observer.validity  import ValidityChangedSubject
from sitebuilder.observer.action  import ActionPerformedSubject
from sitebuilder.observer.action  import ActionPerformedObserver


class BaseControlAgent(ValidityChangedSubject, ValidityChangedObserver,
                       ActionPerformedObserver):
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

        ValidityChangedSubject.__init__(self)
        self._read_only = read_only

    def validity_changed(self, event=None):
        """
        ValidityChangedObserver trigger mmethod local implementation

        Default behaviour is to forwards ValidityChangedEvent to other
        components such as upper level controll agents.
        """
        self.notify_validity_changed(event)

    def get_validity_flag(self):
        """
        Returns component's valididty flag
        """
        # TODO: check that presentation agent instance has been initialized
        return self._presentation_agent.get_validity_flag()

    def set_read_only_flag(self, read_only):
        """
        Sets read only flag
        """
        # TODO: perform type check on read only
        self._read_only = read_only

    def get_read_only_flag(self):
        """
        Returns read only flag
        """
        return self._read_only

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
        # Clears observers lists
        self.clear_validity_changed_observers()

        # Destroyes presentation
        self.get_presentation_agent().destroy()
