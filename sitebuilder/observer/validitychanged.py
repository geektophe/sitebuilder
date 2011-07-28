#!/usr/bin/env python
"""
Observer classes associated with the ValidityChanged events
"""

from sitebuilder.utils.event import Event


class ValidityChangedListener(object):
    """
    Listener object that may be called when a component value has been changed,
    its validity has changed and an action is needed from other components to
    take it in account.
    """

    def validity_changed(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class ValidityChangedDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch validity
    changed events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._validity_changed_listeners = []

    def add_validity_changed_listener(self, listener):
        """
        Adds a ValidityChangedListener listener object to listeners list

        We may add a DataChangedListener instance

        >>> dispatcher = ValidityChangedDispatcher()
        >>> listener = ValidityChangedListener()
        >>> dispatcher.add_validity_changed_listener(listener)

        Adding an object that is not a ValidityChangedListener should raise an
        exception

        >>> dispatcher = ValidityChangedDispatcher()
        >>> dispatcher.add_validity_changed_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of ValidityChangedListener
        """
        if not isinstance(listener, ValidityChangedListener):
            raise AttributeError(
                "Listener must be an instance of ValidityChangedListener")
        self._validity_changed_listeners.append(listener)

    def remove_validity_changed_listener(self, listener):
        """
        Deletes a ValidityChangedListener listener object to listeners list
        """
        try:
            self._validity_changed_listeners.remove(listener)
        except ValueError:
            pass

    def clear_validity_changed_listeners(self):
        """
        Deletes all ValidityChangedListener listeners object from listeners list
        """
        del self._validity_changed_listeners[:]

    def notify_validity_changed(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the ValidityChangedListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = ValidityChangedDispatcher()
        >>> listener = ValidityChangedListener()
        >>> dispatcher.add_validity_changed_listener(listener)
        >>> dispatcher.notify_validity_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_validity_changed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_validity_changed('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._validity_changed_listeners:
            listener.validity_changed(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
