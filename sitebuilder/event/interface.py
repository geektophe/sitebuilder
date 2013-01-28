#!/usr/bin/env python
"""
IEvent interface.

Events may represent various event types (user interaction, system, ui,
and so on) and have to be published in an event bus.

Subscribers on this bus will be called a callback which argument is the event
object.

Specialized event classes have to implement the IEvent interface to be
published on the bus.
"""

from zope.interface import Interface, Attribute

class IEvent(Interface):
    """
    Represents data, user or system events.

    Events have a source (the object that published the event), and may present
    an arbutrary number oh additional attributes.
    """

    source = Attribute(u'The instance that emitted the event')


class IEventBroker(Interface):
    """
    A class that publishes events through an event bus.
    """

    def get_event_bus():
        """
        Returns an event bus on which IEvents are published.
        """
