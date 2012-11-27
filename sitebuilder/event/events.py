#!/usr/bin/env python
"""
Event base class.

Event classes may represent various event types (user interaction, system, ui,
and so on) and have to be published in an event bus.

Subscribers on this bus will be called a callback which argument is the event
object.

Specialized event classes have to subclass this base class to be published on
the bus.
"""

from sitebuiler.event.interface import IEvent
from zope.interface import implements


class BaseEvent(object):
    """
    Base event class.

    An event is represented by its type (class), its source (mandatory
    parameter), and may be specified optional parameters in its parameters
    ditctionnary instance variable.
    """

    implements(IEvent)

    def __init__(self, source, params=None):
        """
        Object initialization.

        @param source       The instance that generated the event.
        @param params       A ditctionnar containing optional parameters.
        """
        self.source = source

        if params is None:
            self.params = params
        else:
            self.params = {}

    def get_source(self):
        """
        Returns event source
        """
        return self.source

    def get_params(self):
        """
        Returns parameters dictionnary
        """
        return self.params
