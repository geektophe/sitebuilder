#!/usr/bin/env python
"""
Observer classes associated with the ValidityChanged events
"""

from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from sitebuilder.interfaces.validity import IValiditySubject, IValidityObserver
from sitebuilder.interfaces.validity import IValidityChangedEvent


class ValidityChangedEvent(object):
    """
    Event class used to notify a validity state changed event.
    """
    implements(IValidityChangedEvent)

    state = FieldProperty(IValidityChangedEvent['state'])
    source_id = FieldProperty(IValidityChangedEvent['source_id'])

    def __init__(self, state, source_id=None):
        """
        The event takes the attribute object that has been changed as
        parameter.
        """
        self.state = state
        self.source_id = source_id


class ValiditySubject(object):
    """
    Subject base class to handle Validity events

    >>> class TestObserver(object):
    ...     implements(IValidityObserver)
    ...     notified = False
    ...     def validity_changed(self, validity):
    ...         self.notified = True
    ...
    >>> subject = ValiditySubject()
    >>> observer = TestObserver()
    >>> subject.register_validity_observer(observer)
    >>> subject.notify_validity_changed(ValidityChangedEvent(True, 1))
    >>> observer.notified
    True

    Adding an object that does not implement IValidityObserver should raise
    an exception

    >>> subject.register_validity_observer('fake')
    Traceback (most recent call last):
        ...
    AttributeError: Observer should implement IValidityObserver

    Notified object should implement IValidityObserver. If not so, an
    exception should be risen

    >>> subject.notify_validity_changed('fake')
    Traceback (most recent call last):
        ...
    AttributeError: event parameter should implement IValidityChandEvent
    """

    implements(IValiditySubject)

    def __init__(self):
        """
        Subject initialization
        """
        self._validity_observers = []

    def register_validity_observer(self, observer):
        """
        Adds a ValidityObserver observer object to observers list
        """
        if not IValidityObserver.providedBy(observer):
            raise AttributeError("Observer should implement IValidityObserver")
        self._validity_observers.append(observer)

    def remove_validity_observer(self, observer):
        """
        Deletes a ValidityObserver observer object to observers list
        """
        try:
            self._validity_observers.remove(observer)
        except ValueError:
            pass

    def clear_validity_observers(self):
        """
        Deletes all AddValidityListener observers object from observers
        list
        """
        del self._validity_observers[:]

    def notify_validity_changed(self, event=None):
        """
        Notifies all observers that that an validity has been changed
        """
        if event is not None and not IValidityChangedEvent.providedBy(event):
            raise AttributeError("event parameter should implement IValidityChandEvent")

        for observer in self._validity_observers:
            observer.validity_changed(event)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
