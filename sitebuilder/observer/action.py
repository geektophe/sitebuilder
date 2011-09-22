#!/usr/bin/env python
"""
Observer classes associated with the ActionPerformed events
"""

class ActionPerformedEvent(object):
    """
    Event class used to notify an attribute changed event.
    """

    def __init__(self, action_name, data=None):
        """
        The event takes the attribute object that has been changed as
        parameter.
        """
        self._action_name = action_name
        self._data = data

    def get_action_name(self):
        """
        Returns trigered action name
        """
        return self._action_name

    def get_data(self):
        """
        Returns action data
        """
        return self._action_name


class ActionPerformedObserver(object):
    """
    Observer class that may be called when an an action has been trigered in an
    user interface.
    """

    def action_performed(self, action_name, data=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class ActionPerformedSubject(object):
    """
    Subject base class that objects may subclass to dispatch
    'attribute changed' events.
    """

    def __init__(self):
        """
        Subject initialization
        """
        self._action_performed_observers = []

    def register_action_performed_observer(self, observer):
        """
        Adds a ActionPerformedObserver observer object to observers list

        We may add a ActionPerformedObserver instance

        >>> subject = ActionPerformedSubject()
        >>> observer = ActionPerformedObserver()
        >>> subject.register_action_performed_observer(observer)

        Adding an object that is not a ActionPerformedObserver should raise an
        exception

        >>> subject = ActionPerformedSubject()
        >>> subject.register_action_performed_observer('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of ActionPerformedObserver
        """
        if not isinstance(observer, ActionPerformedObserver):
            raise AttributeError(
                "Listener must be an instance of ActionPerformedObserver")
        self._action_performed_observers.append(observer)

    def remove_action_performed_observer(self, observer):
        """
        Deletes a ActionPerformedObserver observer object to observers list
        """
        try:
            self._action_performed_observers.remove(observer)
        except ValueError:
            pass

    def clear_action_performed_observers(self):
        """
        Deletes all AddActionActivatedListener observers object from observers
        list
        """
        del self._action_performed_observers[:]

    def notify_action_performed(self, event):
        """
        Notifies all observers that a data has changed

        As the ActionPerformedObserver instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> subject = ActionPerformedSubject()
        >>> observer = ActionPerformedObserver()
        >>> subject.register_action_performed_observer(observer)
        >>> event = ActionPerformedEvent('test')
        >>> subject.notify_action_performed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to observers

        >>> event = ActionPerformedEvent('test')
        >>> subject.notify_action_performed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> subject.notify_action_performed('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of ActionPerformedEvent
        """
        if event is not None and not isinstance(event, ActionPerformedEvent):
            raise AttributeError("event parameter should be an instance " + \
                                 "of ActionPerformedEvent")

        for observer in self._action_performed_observers:
            observer.action_performed(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
