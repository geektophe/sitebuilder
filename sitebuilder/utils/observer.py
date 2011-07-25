#!/usr/bin/env python
"""
This module defines sever listener classes used at different applicaiton
levels.
"""

class DataChangedListener(object):
    """
    Listener object that may be called when a model data has been changed and
    an action is needed from other components to take it in account.
    """

    def data_changed(self):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class DataChangedDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch data changed
    events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._data_changed_listeners = []

    def add_data_changed_listener(self, listener):
        """
        Adds a DataChangedListener listener objetc to listeners list

        We may add a DataChangedListener instance

        >>> controller = DataChangedDispatcher()
        >>> listener = DataChangedListener()
        >>> controller.add_data_changed_listener(listener)

        Adding an object that is not a DataChangedListener should raise an
        exception

        >>> controller = DataChangedDispatcher()
        >>> controller.add_data_changed_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of DataChangedListener
        """
        if not isinstance(listener, DataChangedListener):
            raise AttributeError(
                "Listener must be an instance of DataChangedListener")
        self._data_changed_listeners.append(listener)

    def del_data_changed_listener(self, listener):
        """
        Deletes a DataChangedListener listener objetc to listeners list
        """
        try:
            self._data_changed_listeners.remove(listener)
        except ValueError:
            pass

    def notify_data_changed(self):
        """
        Notifies all listeners that a data has changed

        As the DataChangedListener insntace we use for the test is only used as
        an abstract class, the notify method should raise a NotImplementedError

        >>> controller = DataChangedDispatcher()
        >>> listener = DataChangedListener()
        >>> controller.add_data_changed_listener(listener)
        >>> controller.notify_data_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden
        """
        for listener in self._data_changed_listeners:
            listener.data_changed()


class ValidityChangedListener(object):
    """
    Listener object that may be called when a component value has been changed,
    its validity has changed and an action is needed from other components to
    take it in account.
    """

    def validity_changed(self):
        """
        This method has to be overridden by listeners implementations
        """
        raise NotImplementedError("This method has currently no " + \
                                  "implmentation and has to be overridden")


class ValidityChangedDispatcher(object):
    """
    Dispatcher base class that objects may subclass to dispatch validity
    changed events.
    """

    def __init__(self):
        """
        Dispatcher initialization
        """
        self._validity_changed_listeners = []

    def add_validity_changed_listener(self, listener):
        """
        Adds a ValidityChangedListener listener objetc to listeners list

        We may add a DataChangedListener instance

        >>> controller = ValidityChangedDispatcher()
        >>> listener = ValidityChangedListener()
        >>> controller.add_validity_changed_listener(listener)

        Adding an object that is not a ValidityChangedListener should raise an
        exception

        >>> controller = ValidityChangedDispatcher()
        >>> controller.add_validity_changed_listener('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Listener must be an instance of ValidityChangedListener
        """
        if not isinstance(listener, ValidityChangedListener):
            raise AttributeError(
                "Listener must be an instance of ValidityChangedListener")
        self._validity_changed_listeners.append(listener)

    def del_validity_changed_listener(self, listener):
        """
        Deletes a ValidityChangedListener listener objetc to listeners list
        """
        try:
            self._validity_changed_listeners.remove(listener)
        except ValueError:
            pass

    def notify_validity_changed(self):
        """
        Notifies all listeners that a data has changed

        As the ValidityChangedListener insntace we use for the test is only
        used as an abstract class, the notify method should raise a
        NotImplementedError

        >>> controller = ValidityChangedDispatcher()
        >>> listener = ValidityChangedListener()
        >>> controller.add_validity_changed_listener(listener)
        >>> controller.notify_validity_changed()
        Traceback (most recent call last):
            ...
        NotImplementedError: This method has currently no implmentation and has to be overridden
        """
        for listener in self._validity_changed_listeners:
            listener.validity_changed()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
