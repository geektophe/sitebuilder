#!/usr/bin/env python
"""
Observer classes associated with the Log events
"""

from zope.interface import Interface, implements


class ILogObserver(Interface):
    """
    Observers methods are called when events are logged.
    """

    def event_logged(text):
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

class LogSubject(object):
    """
    Subject base class to handle Log events

    >>> class TestObserver(object):
    ...     implements(ILogObserver)
    ...     notified = False
    ...     def event_logged(self, text):
    ...         self.notified = True
    ...
    >>> subject = LogSubject()
    >>> observer = TestObserver()
    >>> subject.register_log_observer(observer)
    >>> subject.notify_event_logged(u'test')
    >>> observer.notified
    True

    Adding an object that does not implement ILogObserver should raise
    an exception

    >>> subject.register_log_observer('fake')
    Traceback (most recent call last):
        ...
    AttributeError: Observer should implement ILogObserver
    """

    implements(ILogSubject)

    def __init__(self):
        """
        Subject initialization
        """
        self._log_observers = []

    def register_log_observer(self, observer):
        """
        Adds a LogObserver observer object to observers list
        """
        if not ILogObserver.providedBy(observer):
            raise AttributeError("Observer should implement ILogObserver")
        self._log_observers.append(observer)

    def remove_log_observer(self, observer):
        """
        Deletes a LogObserver observer object to observers list
        """
        try:
            self._log_observers.remove(observer)
        except ValueError:
            pass

    def clear_log_observers(self):
        """
        Deletes all AddLogListener observers object from observers
        list
        """
        del self._log_observers[:]

    def notify_event_logged(self, text):
        """
        Notifies all observers that that an log has been changed
        """
        for observer in self._log_observers:
            observer.event_logged(text)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
