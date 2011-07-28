#!/usr/bin/env python
"""
Observer classes associated with the SubmitAction events
"""

from sitebuilder.utils.event import Event


class SubmitActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def submit_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class SubmitActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'submit action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._submit_action_activated_listeners = []

    def add_submit_action_activated_listener(self, listener):
        """
        Submits a SubmitActionListener listener object to listeners list

        We may submit a SubmitActionListener instance

        >>> dispatcher = SubmitActionDispatcher()
        >>> listener = SubmitActionListener()
        >>> dispatcher.add_submit_action_activated_listener(listener)

        Submiting an object that is not a SubmitActionListener should raise an
        exception

        >>> dispatcher = SubmitActionDispatcher()
        >>> dispatcher.add_submit_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of SubmitActionListener
        """
        if not isinstance(listener, SubmitActionListener):
            raise AttributeError(
                "Listener must be an instance of SubmitActionListener")
        self._submit_action_activated_listeners.append(listener)

    def remove_submit_action_activated_listener(self, listener):
        """
        Submits a SubmitActionListener listener object to listeners list
        """
        try:
            self._submit_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_submit_action_activated_listeners(self):
        """
        Deletes all SubmitActionActivatedListener listeners object from
        listeners list
        """
        del self._submit_action_activated_listeners[:]

    def notify_submit_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the SubmitActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = SubmitActionDispatcher()
        >>> listener = SubmitActionListener()
        >>> dispatcher.add_submit_action_activated_listener(listener)
        >>> dispatcher.notify_submit_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_submit_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_submit_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._submit_action_activated_listeners:
            listener.submit_action_activated(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
