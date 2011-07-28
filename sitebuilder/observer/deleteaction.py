#!/usr/bin/env python
"""
Observer classes associated with the DeleteAction events
"""

from sitebuilder.utils.event import Event


class DeleteActionListener(object):
    """
    Listener object that may be called when the view action is activated in
    a view.
    """

    def delete_action_activated(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class DeleteActionDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch
    'delete action activated' events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._delete_action_activated_listeners = []

    def add_delete_action_activated_listener(self, listener):
        """
        Deletes a DeleteActionListener listener object to listeners list

        We may delete a DeleteActionListener instance

        >>> dispatcher = DeleteActionDispatcher()
        >>> listener = DeleteActionListener()
        >>> dispatcher.add_delete_action_activated_listener(listener)

        Deleteing an object that is not a DeleteActionListener should raise an
        exception

        >>> dispatcher = DeleteActionDispatcher()
        >>> dispatcher.add_delete_action_activated_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of DeleteActionListener
        """
        if not isinstance(listener, DeleteActionListener):
            raise AttributeError(
                "Listener must be an instance of DeleteActionListener")
        self._delete_action_activated_listeners.append(listener)

    def remove_delete_action_activated_listener(self, listener):
        """
        Deletes a DeleteActionListener listener object to listeners list
        """
        try:
            self._delete_action_activated_listeners.remove(listener)
        except ValueError:
            pass

    def clear_delete_action_activated_listeners(self):
        """
        Deletes all DeleteActionActivatedListener listeners object from
        listeners list
        """
        del self._delete_action_activated_listeners[:]

    def notify_delete_action_activated(self, event=None):
        """
        Notifies all listeners that a data has changed

        As the DeleteActionListener instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> dispatcher = DeleteActionDispatcher()
        >>> listener = DeleteActionListener()
        >>> dispatcher.add_delete_action_activated_listener(listener)
        >>> dispatcher.notify_delete_action_activated()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to listeners

        >>> event = Event('test')
        >>> dispatcher.notify_delete_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> dispatcher.notify_delete_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of Event
        """
        if not event is None and not isinstance(event, Event):
            raise AttributeError("event parameter should be an instance of Event")

        for listener in self._delete_action_activated_listeners:
            listener.delete_action_activated(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
