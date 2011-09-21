#!/usr/bin/env python
"""
Observer classes associated with the AttributeChanged events
"""

class AttributeChangedEvent(object):
    """
    Event class used to notify an attribute changed event.
    """

    def __init__(self, attribute=None):
        """
        The event takes the attribute object that has been changed as
        parameter.
        """
        self._attribute = attribute

    def get_attribute(self):
        """
        Returns attached attribute instance
        """
        return self._attribute


class AttributeChangedObserver(object):
    """
    Observer class that may be called when an attribute has been changed and
    an action is needed from other components to take it in account.
    """

    def attribute_changed(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class AttributeChangedSubject(object):
    """
    Subject base class that objects may subclass to dispatch
    'attribute changed' events.
    """

    def __init__(self):
        """
        Subject initialization
        """
        self._attribute_changed_observers = []

    def register_attribute_changed_observer(self, observer):
        """
        Adds a AttributeChangedObserver observer object to observers list

        We may add a AttributeChangedObserver instance

        >>> subject = AttributeChangedSubject()
        >>> observer = AttributeChangedObserver()
        >>> subject.register_attribute_changed_observer(observer)

        Adding an object that is not a AttributeChangedObserver should raise an
        exception

        >>> subject = AttributeChangedSubject()
        >>> subject.register_attribute_changed_observer('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of AttributeChangedObserver
        """
        if not isinstance(observer, AttributeChangedObserver):
            raise AttributeError(
                "Listener must be an instance of AttributeChangedObserver")
        self._attribute_changed_observers.append(observer)

    def remove_attribute_changed_observer(self, observer):
        """
        Deletes a AttributeChangedObserver observer object to observers list
        """
        try:
            self._attribute_changed_observers.remove(observer)
        except ValueError:
            pass

    def clear_attribute_changed_observers(self):
        """
        Deletes all AddActionActivatedListener observers object from observers
        list
        """
        del self._attribute_changed_observers[:]

    def notify_attribute_changed(self, event=None):
        """
        Notifies all observers that a data has changed

        As the AttributeChangedObserver instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> subject = AttributeChangedSubject()
        >>> observer = AttributeChangedObserver()
        >>> subject.register_attribute_changed_observer(observer)
        >>> subject.notify_attribute_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to observers

        >>> event = AttributeChangedEvent('test')
        >>> subject.notify_attribute_changed(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> subject.notify_attribute_changed('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of AttributeChangedEvent
        """
        if event is not None and not isinstance(event, AttributeChangedEvent):
            raise AttributeError("event parameter should be an instance " + \
                                 "of AttributeChangedEvent")

        for observer in self._attribute_changed_observers:
            observer.attribute_changed(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
