#!/usr/bin/env python
"""
Base control Agent class to be subclassed
"""

from sitebuilder.presentation.interface import IPresentationAgent
from sitebuilder.exception import FieldFormatError
from sitebuilder.event.bus import EventBus
from zope.schema import ValidationError
from zope.interface import providedBy


class BaseControlAgent(object):
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
        self._presentation_agent = None
        self._site = None
        self._event_bus = EventBus()

    def get_event_bus(self):
        """
        Returns component's event bus.
        """
        return self._event_bus

    def get_read_only_flag(self):
        """
        Returns read only flag
        """
        return self._read_only

    get_read_only = get_read_only_flag

    def set_read_only_flag(self, read_only):
        """
        Returns read only flag
        """
        if not read_only is True and not read_only is False:
            raise TypeError("read only flag should be a boolean value")

        self._read_only = read_only

    set_read_only = set_read_only_flag

    def set_presentation_agent(self, presentation_agent):
        """
        Sets local PresentationAgent implementation instance
        """
        # TODO: perform better instance check on presentation agent
        if not IPresentationAgent.providedBy(presentation_agent):
            raise AttributeError("presentation agent should implement " +
                                 "IPresentationAgent")

        self._presentation_agent = presentation_agent

    def get_presentation_agent(self):
        """
        Returns local PresentationAgent implementation instance
        """
        return self._presentation_agent

    def set_site(self, site):
        """
        Returns local PresentationAgent implementation instance
        """
        # TODO: perform instance check on site
        self._site = site

    def get_site(self):
        """
        Returns site instance
        """
        return self._site

    def get_attribute_value(self, name):
        """
        Returns a site attribute value

        As views do not allow None values, an empty string is returnd in place
        """
        # TODO: check that presentation agent instance has been initialized
        value = getattr(self._site, name)

        if value is not None:
            return value
        else:
            return u''

    get_value = get_attribute_value

    def set_attribute_value(self, name, value):
        """
        Returns a site attribute value
        """
        try:
            setattr(self._site, name, value)
        except ValidationError, e:

            for interface in providedBy(self._site):
                field = interface.get(name)

                if field is not None:
                    # Use the field description attribute to give the user a
                    # relevant error message
                    try:
                        raise FieldFormatError(field.description)
                    except AttributeError:
                        raise e

            # No field was found under name. The original exception is risen
            raise e

    set_value = set_attribute_value

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Destroyes presentation
        self.get_presentation_agent().destroy()
