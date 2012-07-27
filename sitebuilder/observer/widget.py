#!/usr/bin/env python
"""
Observer classes associated with GUI widgets actions.

Any followable widget should trigger widget_changed observer method when set.
"""

from zope.interface import Interface, implements


class IWidgetObserver(Interface):
    """
    Observers methods are called on widget data changed event.
    """

    def widget_changed(name, value):
        """
        Observer method run on widget changed event

        Name is the name of the widget that triggerd the event, value is the
        value it was set to.
        """


class IWidgetSubject(Interface):
    """
    Subject notify observers on widget events
    """

    def register_widget_observer(observer):
        """
        Adds a WidgetObserver observer object to observers list
        """

    def remove_widget_observer(observer):
        """
        Deletes a WidgetObserver observer object to observers list
        """

    def clear_widget_observers():
        """
        Deletes all observers object from observers list
        """

    def notify_widget_changed(widget):
        """
        Notifies all observers that a data has changed
        """


class WidgetSubject(object):
    """
    Subject base class to handle Widget events

    >>> class TestObserver(object):
    ...     implements(IWidgetObserver)
    ...     notified = False
    ...     def widget_changed(self, name, value):
    ...         self.notified = True
    ...
    >>> subject = WidgetSubject()
    >>> observer = TestObserver()
    >>> subject.register_widget_observer(observer)
    >>> subject.notify_widget_changed('widget', u'test')
    >>> observer.notified
    True

    Adding an object that does not implement IWidgetObserver should raise
    an exception

    >>> subject.register_widget_observer('fake')
    Traceback (most recent call last):
        ...
    ValueError: Observer should implement IWidgetObserver
    """

    implements(IWidgetSubject)

    def __init__(self):
        """
        Subject initialization
        """
        self._widget_observers = []

    def register_widget_observer(self, observer):
        """
        Adds a WidgetObserver observer object to observers list
        """
        if not IWidgetObserver.providedBy(observer):
            raise ValueError("Observer should implement IWidgetObserver")
        self._widget_observers.append(observer)

    def remove_widget_observer(self, observer):
        """
        Deletes a WidgetObserver observer object to observers list
        """
        try:
            self._widget_observers.remove(observer)
        except ValueError:
            pass

    def clear_widget_observers(self):
        """
        Deletes all WidgetListener observers object from observers
        list
        """
        del self._widget_observers[:]

    def notify_widget_changed(self, name, value):
        """
        Notifies all observers that that an widget has been changed
        """
        for observer in self._widget_observers:
            observer.widget_changed(name, value)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

