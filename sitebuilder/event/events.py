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

from sitebuilder.event.interface import IEvent
from zope.interface import implements


class BaseEvent(object):
    """
    Base event class.

    An event is represented by its type (class), its source (mandatory
    parameter), and may be specified optional parameters in the contructor
    that are mapped into instance variables.

    For enstance :

    >>> event = BaseEvent(__name__, parm1=1, parm2=2)
    >>> event.source == __name__
    True
    >>> event.parm1
    1
    >>> event.parm2
    2
    """

    implements(IEvent)

    def __init__(self, source, **kwargs):
        """
        Object initialization.

        @param source       The instance that generated the event.
        @param kwargs       A ditctionnary containing optional parameters to be
                            mapped as instance variables.
        """
        self.source = source

        for key, value in kwargs.items():
            setattr(self, key, value)


class UIActiondEvent(BaseEvent):
    """
    Event sent when an UI action (action mapped to a button click or a menu
    item selection, and so on...) has been triggerd.

    Event attributes:

        action  The action identifier
    """
    action = None

class UIWidgetEvent(BaseEvent):
    """
    Event sent when an UI widget state changed (text box has been set, radio
    button has been selected, and so on...).

    Event params keys:

        name  The widget name that has been changed
        value The widget value set
    """
    name = None
    value = None


if __name__ == '__main__':
    import doctest
    doctest.testmod()
