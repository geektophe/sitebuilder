#!/usr/bin/env python
"""
Observer classes associated with the Attribute events
"""

from zope.interface import implements
from sitebuilder.interfaces.attribute import IAttributeSubject, IAttributeObserver


class AttributeSubject(object):
    """
    Subject base class to handle Attribute events
    """

    implements(IAttributeSubject)

    def __init__(self):
        """
        Subject initialization
        """
        self._attribute_observers = []

    def register_attribute_observer(self, observer):
        """
        Adds a AttributeObserver observer object to observers list

        We may add a AttributeObserver instance

        >>> class TestObserver(object):
        ...     implements(IAttributeObserver)
        ...     notified = False
        ...     def attribute_changed(self, attribute):
        ...         self.notified = True
        ...
        >>> subject = AttributeSubject()
        >>> observer = TestObserver()
        >>> subject.register_attribute_observer(observer)
        >>> subject.notify_attribute_changed(u'test')
        >>> observer.notified
        True

        Adding an object that does not implement IAttributeObserver should raise
        an exception

        >>> subject.register_attribute_observer('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Observer should implement IAttributeObserver
        """
        if not IAttributeObserver.providedBy(observer):
            raise AttributeError("Observer should implement IAttributeObserver")
        self._attribute_observers.append(observer)

    def remove_attribute_observer(self, observer):
        """
        Deletes a AttributeObserver observer object to observers list
        """
        try:
            self._attribute_observers.remove(observer)
        except ValueError:
            pass

    def clear_attribute_observers(self):
        """
        Deletes all AddAttributeListener observers object from observers
        list
        """
        del self._attribute_observers[:]

    def notify_attribute_changed(self, attribute=None):
        """
        Notifies all observers that that an attribute has been changed
        """
        for observer in self._attribute_observers:
            observer.attribute_changed(attribute)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
