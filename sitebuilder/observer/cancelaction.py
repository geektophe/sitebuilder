#!/usr/bin/env python
"""
Observer classes associated with the CancelAction events
"""

from sitebuilder.utils.event import Event


class CancelActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def cancel_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class CancelActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'cancel action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._cancel_action_activated_listeners = []

    def add_cancel_action_activated_listener(self, listener):
        """
        Submits a CancelActionListener listener object to listeners list

        We may cancel a CancelActionListener instance

        >>> dispatcher = CancelActionDispatcher()
        >>> listener = CancelActionListener()
        >>> dispatcher.add_cancel_action_activated_listener(listener)

        Submiting an object that is not a CancelActionListener should raise an
        exception

        >>> dispatcher = CancelActionDispatcher()
        >>> dispatcher.add_cancel_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of CancelActionListener
        """
        if not isinstance(listener, CancelActionListener):
            raise AttributeError(
                "Listener must be an instance of CancelActionListener")
        self._cancel_action_activated_listeners.append(listener)

    def remove_cancel_action_activated_listener(self, listener):
        """
        Submits a CancelActionListener listener object to listeners list
        """
        try:
            self._cancel_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_cancel_action_activated_listeners(self):
        """
        Deletes all CancelActionActivatedListener listeners object from
        listeners list
        """
        del self._cancel_action_activated_listeners[:]

    def notify_cancel_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the CancelActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = CancelActionDispatcher()
        >>> listener = CancelActionListener()
        >>> dispatcher.add_cancel_action_activated_listener(listener)
        >>> dispatcher.notify_cancel_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_cancel_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_cancel_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._cancel_action_activated_listeners:
            listener.cancel_action_activated(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
