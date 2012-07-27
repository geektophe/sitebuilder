#!/usr/bin/env python
"""
Observer classes associated with the ValidityChanged events
"""

from zope.interface import Interface, implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema import Bool, Int


class IValidityObserver(Interface):
    """
    Observers methods are called on validity validity event.
    """

    def validity_changed(source, flag):
        """
        Observer method run on validity changed event
        """


class IValiditySubject(Interface):
    """
    Subject notify observers on validity events
    """

    def register_validity_observer(observer):
        """
        Adds a ValidityActivatedObserver observer object to observers list
        """

    def remove_validity_observer(observer):
        """
        Deletes a ValidityActivatedObserver observer object to observers list
        """

    def clear_validity_observers():
        """
        Deletes all observers object from observers list
        """

    def notify_validity_changed(flag):
        """
        Notifies all observers that a data has changed
        """


class ValiditySubject(object):
    """
    Subject base class to handle Validity events

    >>> class TestObserver(object):
    ...     implements(IValidityObserver)
    ...     notified = False
    ...     def validity_changed(self, source, flag):
    ...         self.notified = True
    ...
    >>> subject = ValiditySubject()
    >>> observer = TestObserver()
    >>> subject.register_validity_observer(observer)
    >>> subject.notify_validity_changed(True)
    >>> observer.notified
    True

    Adding an object that does not implement IValidityObserver should raise
    an exception

    >>> subject.register_validity_observer('fake')
    Traceback (most recent call last):
        ...
    AttributeError: Observer should implement IValidityObserver
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

    def notify_validity_changed(self, flag):
        """
        Notifies all observers that that an validity has been changed
        """
        for observer in self._validity_observers:
            observer.validity_changed(self, flag)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
