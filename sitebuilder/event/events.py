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


class UIActionEvent(BaseEvent):
    """
    Event sent when an UI action (action mapped to a button click or a menu
    item selection, and so on...) has been triggerd.

    Event attributes:

        action      The acion name that has been changed
        parameters  The acton optional parameters (may be any type)
    """
    action = None
    parameters = None


class UIWidgetEvent(BaseEvent):
    """
    Event sent when an UI widget state changed (text box has been set, radio
    button has been selected, and so on...).

    Event attributes:


        name  The widget name that has been changed
        value The widget value set
    """
    name = None
    value = None


class DataValidityEvent(BaseEvent):
    """
    Event sent when a user tried to set an invalid data into a data structure,
    or when the correct value was set afterwards.

    Event attributes:


        attribute   The atribute name that has been changed
        flag        The flag indicating if the atribute was correctly or
                    incorrectly set.
    """
    attribute = None
    flag = None


class DataChangeEvent(BaseEvent):
    """
    Event sent when a user tried to set an invalid data into a data structure,
    or when the correct value was set afterwards.

    Event attributes:


        attribute   The atribute name that has been changed
        flag        The flag indicating if the atribute was correctly or
                    incorrectly set.
    """
    name = None
    value = None


class AppActionEvent(BaseEvent):
    """
    Event sent by application when internal actions are triggerred.

    Event attributes:


        action      The acion name that has been changed
        parameters  The acton optional parameters (may be any type)
    """
    action = None
    parameters = None


class CommandExecEvent(BaseEvent):
    """
    Event sent by application when a command has been executed.
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod()
