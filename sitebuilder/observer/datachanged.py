#!/usr/bin/env python
"""
Observer classes associated with the DataChanged events
"""

from sitebuilder.utils.event import Event


class DataChangedListener(object):
    """
    Listener object that may be called when a model data has been changed and
    an action is needed from other components to take it in account.
    """

    def data_changed(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class DataChangedDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch data changed
    events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._data_changed_listeners = []

    def add_data_changed_listener(self, listener):
        """
        Adds a DataChangedListener listener object to listeners list

        We may add a DataChangedListener instance

        >>> dispatcher = DataChangedDispatcher()
        >>> listener = DataChangedListener()
        >>> dispatcher.add_data_changed_listener(listener)

        Adding an object that is not a DataChangedListener should raise an
        exception

        >>> dispatcher = DataChangedDispatcher()
        >>> dispatcher.add_data_changed_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of DataChangedListener
        """
        if not isinstance(listener, DataChangedListener):
            raise AttributeError(
                "Listener must be an instance of DataChangedListener")
        self._data_changed_listeners.append(listener)

    def remove_data_changed_listener(self, listener):
        """
        Deletes a DataChangedListener listener object to listeners list
        """
        try:
            self._data_changed_listeners.remove(listener)
        except ValueError:
            pass

    def clear_data_changed_listeners(self):
        """
        Deletes all DataChangedListener listeners object from listeners list
        """
        del self._data_changed_listeners[:]

    def notify_data_changed(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the DataChangedListener instance we use for the test is only used as
        an abstract class, the notify method should raise a NotImplementedError

        >>> dispatcher = DataChangedDispatcher()
        >>> listener = DataChangedListener()
        >>> dispatcher.add_data_changed_listener(listener)
        >>> dispatcher.notify_data_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_data_changed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_data_changed('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._data_changed_listeners:
            listener.data_changed(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
