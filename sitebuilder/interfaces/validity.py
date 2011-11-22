#!/usr/bin/env python
"""
ValidityChanged observer interace
"""

from zope.interface import Interface
from zope.schema import Bool, Int


class IValidityChangedEvent(Interface):
    """
    Event class used to notify a validity state changed event.
    """
    state  = Bool(title=u"Validity state")
    source_id  = Int(title=u"Event source id")


class IValidityObserver(Interface):
    """
    Observers methods are called on validity validity event.
    """

    def validity_changed(self, state):
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

    def notify_validity_changed(state):
        """
        Notifies all observers that a data has changed
        """
