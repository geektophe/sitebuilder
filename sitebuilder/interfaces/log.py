#!/usr/bin/env python
"""
LogActivated observer interace
"""

from zope.interface import Interface


class ILogObserver(Interface):
    """
    Observers methods are called when events are logged.
    """

    def event_logged(self, text):
        """
        Observer method run on log event
        """


class ILogSubject(Interface):
    """
    Subject notify observers on log events
    """

    def register_log_observer(observer):
        """
        Adds a LogActivatedObserver observer object to observers list
        """

    def remove_log_observer(observer):
        """
        Deletes a LogActivatedObserver observer object to observers list
        """

    def clear_log_observers():
        """
        Deletes all observers object from observers list
        """

    def notify_event_logged(text):
        """
        Notifies all observers that a data has changed
        """
