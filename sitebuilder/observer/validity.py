#!/usr/bin/env python
"""
Observer classes associated with the ValidityChanged events
"""

class ValidityChangedEvent(object):
    """
    Event class used to notify a validity state changed event.
    """

    def __init__(self, state, source_id=None):
        """
        The event takes the attribute object that has been changed as
        parameter.
        """
        self._state = state
        self._source_id = source_id

    def get_state(self):
        """
        Returns attached attribute instance
        """
        return self._state

    def get_source_id(self):
        """
        Returns the event source id hash. It may be used to build a matrix
        components validity.
        """
        return self._source_id


class ValidityChangedObserver(object):
    """
    Observer class that may be called when a validity state has been changed
    and an action is needed from other components to take it in account.
    """

    def validity_changed(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class ValidityChangedSubject(object):
    """
    Subject base class that objects may subclass to dispatch
    'validity state changed' events.
    """

    def __init__(self):
        """
        Subject initialization
        """
        self._validity_changed_observers = []

    def register_validity_changed_observer(self, observer):
        """
        Adds a ValidityChangedObserver observer object to observers list

        We may add a ValidityChangedObserver instance

        >>> subject = ValidityChangedSubject()
        >>> observer = ValidityChangedObserver()
        >>> subject.register_validity_changed_observer(observer)

        Adding an object that is not a ValidityChangedObserver should raise an
        exception

        >>> subject = ValidityChangedSubject()
        >>> subject.register_validity_changed_observer('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of ValidityChangedObserver
        """
        if not isinstance(observer, ValidityChangedObserver):
            raise AttributeError(
                "Listener must be an instance of ValidityChangedObserver")
        self._validity_changed_observers.append(observer)

    def remove_validity_changed_observer(self, observer):
        """
        Deletes a ValidityChangedObserver observer object to observers list
        """
        try:
            self._validity_changed_observers.remove(observer)
        except ValueError:
            pass

    def clear_validity_changed_observers(self):
        """
        Deletes all AddActionActivatedListener observers object from observers
        list
        """
        del self._validity_changed_observers[:]

    def notify_validity_changed(self, event=None):
        """
        Notifies all observers that a data has changed

        As the ValidityChangedObserver instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> subject = ValidityChangedSubject()
        >>> observer = ValidityChangedObserver()
        >>> subject.register_validity_changed_observer(observer)
        >>> subject.notify_validity_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to observers

        >>> event = ValidityChangedEvent('test')
        >>> subject.notify_validity_changed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> subject.notify_validity_changed('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of ValidityChangedEvent
        """
        if event is not None and not isinstance(event, ValidityChangedEvent):
            raise AttributeError("event parameter should be an instance " + \
                                 "of ValidityChangedEvent")

        for observer in self._validity_changed_observers:
            observer.validity_changed(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
