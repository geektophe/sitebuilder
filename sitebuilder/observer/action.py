#!/usr/bin/env python
"""
Observer classes associated with the Action events
"""

from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from sitebuilder.interfaces.action import IAction, IActionSubject, IActionObserver

class Action(object):
    """
    Action asked with specific parameters
    """
    implements(IAction)

    name = FieldProperty(IAction['name'])
    parameters = FieldProperty(IAction['parameters'])


    def __init__(self, name, parameters={}):
        """
        The event take action name and its associated parameters as arguments.

        Name is a string representing the action type.
        Parameters, if set, should be an instance of dict.
        """
        self.name = name
        self.parameters = parameters


class ActionSubject(object):
    """
    Subject base class to handle Action events
    """

    implements(IActionSubject)

    def __init__(self):
        """
        Subject initialization
        """
        self._action_observers = []

    def register_action_observer(self, observer):
        """
        Adds a ActionObserver observer object to observers list

        We may add a ActionObserver instance

        >>> class TestObserver(object):
        ...     implements(IActionObserver)
        ...     notified = False
        ...     def action_activated(self, action):
        ...         self.notified = True
        ...
        >>> subject = ActionSubject()
        >>> observer = TestObserver()
        >>> subject.register_action_observer(observer)
        >>> subject.notify_action_activated(Action(u'test'))
        >>> observer.notified
        True

        Adding an object that does not implement IActionObserver should raise
        an exception

        >>> subject.register_action_observer('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Observer should implement IActionObserver

        Notified object should implement IAction. If not so, an exception
        should be risen
        >>> subject.notify_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: action parameter should implement IAction
        """
        if not IActionObserver.providedBy(observer):
            raise AttributeError("Observer should implement IActionObserver")
        self._action_observers.append(observer)

    def remove_action_observer(self, observer):
        """
        Deletes a ActionObserver observer object to observers list
        """
        try:
            self._action_observers.remove(observer)
        except ValueError:
            pass

    def clear_action_observers(self):
        """
        Deletes all AddActionListener observers object from observers
        list
        """
        del self._action_observers[:]

    def notify_action_activated(self, action=None):
        """
        Notifies all observers that that an action has been activated
        """
        if action is not None and not IAction.providedBy(action):
            raise AttributeError("action parameter should implement IAction")

        for observer in self._action_observers:
            observer.action_activated(action)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
