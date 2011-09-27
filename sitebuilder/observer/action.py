#!/usr/bin/env python
"""
Observer classes associated with the ActionActivated events
"""

class ActionActivatedEvent(object):
    """
    Event class used to notify that a specific action has been asked on a
    configuraiton instance.

    Mainly used for communications between control agents and presentation
    agents to report user actions.

    It contains an action name and an optional parameters object.
    """

    def __init__(self, name, parameters=None):
        """
        The event take action name and its associated parameters as arguments.

        Name is a string representing the action type.
        Parameters, if set, should be an instance of dict.
        """
        if parameters is not None and not isinstance(parameters, dict):
            raise TypeError("parameters should be an instance of dict")

        self._name = name
        self._parameters = parameters

    def get_name(self):
        """
        Returns trigered action name
        """
        return self._name

    def get_parameters(self):
        """
        Returns action parameters
        """
        return self._parameters


class ActionActivatedObserver(object):
    """
    Observer class that may be called when an an action has been trigered in an
    user interface.
    """

    def action_activated(self, action_name, data=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class ActionActivatedSubject(object):
    """
    Subject base class that objects may subclass to dispatch
    'attribute changed' events.
    """

    def __init__(self):
        """
        Subject initialization
        """
        self._action_activated_observers = []

    def register_action_activated_observer(self, observer):
        """
        Adds a ActionActivatedObserver observer object to observers list

        We may add a ActionActivatedObserver instance

        >>> subject = ActionActivatedSubject()
        >>> observer = ActionActivatedObserver()
        >>> subject.register_action_activated_observer(observer)

        Adding an object that is not a ActionActivatedObserver should raise an
        exception

        >>> subject = ActionActivatedSubject()
        >>> subject.register_action_activated_observer('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of ActionActivatedObserver
        """
        if not isinstance(observer, ActionActivatedObserver):
            raise AttributeError(
                "Listener must be an instance of ActionActivatedObserver")
        self._action_activated_observers.append(observer)

    def remove_action_activated_observer(self, observer):
        """
        Deletes a ActionActivatedObserver observer object to observers list
        """
        try:
            self._action_activated_observers.remove(observer)
        except ValueError:
            pass

    def clear_action_activated_observers(self):
        """
        Deletes all AddActionActivatedListener observers object from observers
        list
        """
        del self._action_activated_observers[:]

    def notify_action_activated(self, event):
        """
        Notifies all observers that a data has changed

        As the ActionActivatedObserver instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> subject = ActionActivatedSubject()
        >>> observer = ActionActivatedObserver()
        >>> subject.register_action_activated_observer(observer)
        >>> event = ActionActivatedEvent('test')
        >>> subject.notify_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to observers

        >>> event = ActionActivatedEvent('test')
        >>> subject.notify_action_activated(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> subject.notify_action_activated('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of ActionActivatedEvent
        """
        if event is not None and not isinstance(event, ActionActivatedEvent):
            raise AttributeError("event parameter should be an instance " + \
                                 "of ActionActivatedEvent")

        for observer in self._action_activated_observers:
            observer.action_activated(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
