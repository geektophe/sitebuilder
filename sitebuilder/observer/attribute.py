#!/usr/bin/env python
"""
Observer classes associated with the AttributeChanged events
"""

class AttributeModifiedEvent(object):
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


class AttributeModifiedObserver(object):
    """
    Observer class that may be called when an attribute has been modified and
    an action is needed from other components to take it in account.
    """

    def attribute_modified(self, event=None):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class AttributeModifiedSubject(object):
    """
    Subject base class that objects may subclass to dispatch
    'attribute modified' events.
    """

    def __init__(self):
        """
        Subject initialization
        """
        self._attribute_modified_observers = []

    def register_attribute_modified_observer(self, observer):
        """
        Adds a AttributeModifiedObserver observer object to observers list

        We may add a AttributeModifiedObserver instance

        >>> subject = AttributeModifiedSubject()
        >>> observer = AttributeModifiedObserver()
        >>> subject.register_attribute_modified_observer(observer)

        Adding an object that is not a AttributeModifiedObserver should raise an
        exception

        >>> subject = AttributeModifiedSubject()
        >>> subject.register_attribute_modified_observer('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of AttributeModifiedObserver
        """
        if not isinstance(observer, AttributeModifiedObserver):
            raise AttributeError(
                "Listener must be an instance of AttributeModifiedObserver")
        self._attribute_modified_observers.append(observer)

    def remove_attribute_modified_observer(self, observer):
        """
        Deletes a AttributeModifiedObserver observer object to observers list
        """
        try:
            self._attribute_modified_observers.remove(observer)
        except ValueError:
            pass

    def clear_attribute_modified_observers(self):
        """
        Deletes all AddActionActivatedListener observers object from observers
        list
        """
        del self._attribute_modified_observers[:]

    def notify_attribute_modified(self, event=None):
        """
        Notifies all observers that a data has changed

        As the AttributeModifiedObserver instance we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> subject = AttributeModifiedSubject()
        >>> observer = AttributeModifiedObserver()
        >>> subject.register_attribute_modified_observer(observer)
        >>> subject.notify_attribute_modified()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        An event containing the context that triggered the event may also be
        passed to observers

        >>> event = AttributeModifiedEvent('test')
        >>> subject.notify_attribute_modified(event)
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden

        Using a parameter that is not an event shold raise en exception
        >>> subject.notify_attribute_modified('fake')
        Traceback (most recent call last):
            ...
        AttributeError: event parameter should be an instance of AttributeModifiedEvent
        """
        if event is not None and not isinstance(event, AttributeModifiedEvent):
            raise AttributeError("event parameter should be an instance " + \
                                 "of AttributeModifiedEvent")

        for observer in self._attribute_modified_observers:
            observer.attribute_modified(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
