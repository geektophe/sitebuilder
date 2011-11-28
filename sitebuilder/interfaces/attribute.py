#!/usr/bin/env python
"""
AttributeChanged observer interace
"""

from zope.interface import Interface


class IAttributeObserver(Interface):
    """
    Observers methods are called on attribute activaee event.
    """

    def attribute_changed(self, attribute):
        """
        Observer method run on attribute changed event
        """


class IAttributeSubject(Interface):
    """
    Subject notify observers on attribute events
    """

    def register_attribute_observer(observer):
        """
        Adds a AttributeActivatedObserver observer object to observers list
        """

    def remove_attribute_observer(observer):
        """
        Deletes a AttributeActivatedObserver observer object to observers list
        """

    def clear_attribute_observers():
        """
        Deletes all observers object from observers list
        """

    def notify_attribute_changed(attribute):
        """
        Notifies all observers that a data has changed
        """
