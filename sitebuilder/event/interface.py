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
    Base event class.

    An event is represented by its type (class), its source (mandatory
    parameter), and may be specified optional parameters in its parameters
    ditctionnary instance variable.
    """

    source = Attribute(u'The instance that emitted the event')
    params = Attribute(u'An optional parameters dictionnary')

    def get_source():
        """
        Returns event source
        """

    def get_params():
        """
        Returns parameters dictionnary
        """
