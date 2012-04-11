#!/usr/bin/env python
"""
Observer classes associated with the Command events
"""

from zope.interface import Interface, implements


class ICommandObserver(Interface):
    """
    Observers methods are called on command executed event.
    """

    def command_executed(command):
        """
        Observer method run on command avtivated event
        """


class ICommandSubject(Interface):
    """
    Subject notify observers on command events

    Command subject may be used in both ways :

        - Using observer object implementing ICommandObserver, registered
          using register_command_observer method (the safest)

        - Using callback functions (or callable objects), registerd using
          register_command_callback method.

    Prefer using observer objects in standard usage.

    If the same object has to listen to several commands and react differently
    to each one, you may use callbacks.
    """

    def register_command_observer(observer):
        """
        Adds a CommandActivatedObserver observer object to observers list to
        be notified when command execution has finished
        """

    def register_command_callback(callback):
        """
        Adds a callback function (or callable object) to cvallback list to be
        notified when command execution has finished

        Callback signature should be :

            callback(command)

        Where command is the command object itself
        """

    def remove_command_observer(observer):
        """
        Removes a CommandActivatedObserver observer object from observer list
        """

    def remove_command_callback(callback):
        """
        Deletes a callback function (or callable object) from callback list
        """

    def clear_command_observers():
        """
        Removes all observers object from observers list
        """

    def clear_command_callbacks():
        """
        Removes all callback references from callback list
        """

    def notify_command_executed():
        """
        Notifies all observers that the command has been executed
        """


class CommandSubject(object):
    """
    Subject base class to handle Command events

    >>> from zope.schema.fieldproperty import FieldProperty
    >>> from sitebuilder.command.interface import ICommand
    >>> class TestCommand(CommandSubject):
    ...     implements(ICommand, ICommandObserver)
    ...     status = FieldProperty(ICommand['status'])
    ...     return_code = FieldProperty(ICommand['return_code'])
    ...     result = None
    ...     error = None
    ...     exception = None
    ...     def wait(self, timeout=None):
    ...         pass
    ...     def execute(self, driver):
    ...         self.notify_command_executed()
    ...
    >>> class TestObserver(object):
    ...     implements(ICommandObserver)
    ...     notified = False
    ...     def command_executed(self, command):
    ...         self.notified = True
    ...
    >>> command = TestCommand()
    >>> observer = TestObserver()
    >>> command.register_command_observer(observer)
    >>> command.execute(None)
    >>> observer.notified
    True

    Adding an object that does not implement ICommandObserver should raise
    an exception

    >>> command.register_command_observer('fake')
    Traceback (most recent call last):
        ...
    AttributeError: Observer should implement ICommandObserver

    Once observers cleared from subject, they should not be notified anymore

    >>> observer.notified = False
    >>> command.clear_command_observers()
    >>> command.execute(None)
    >>> observer.notified
    False

    It's also possible to use callback functions/methods for specific use

    >>> notified = False
    >>> def test_callback(command):
    ...     global notified
    ...     notified = True
    ...
    >>> command.register_command_callback(test_callback)
    >>> command.execute(None)
    >>> notified
    True

    Once callbacks cleared from subject, they should not be notified anymore

    >>> notified = False
    >>> command.clear_command_callbacks()
    >>> command.execute(None)
    >>> notified
    False
    """

    implements(ICommandSubject)

    def __init__(self):
        """
        Subject initialization
        """
        self._command_callbacks = []

    def register_command_observer(self, observer):
        """
        Adds a CommandActivatedObserver observer object to observers list to
        be notified when command execution has finished
        """
        if not ICommandObserver.providedBy(observer):
            raise AttributeError("Observer should implement ICommandObserver")
        self._command_callbacks.append(observer.command_executed)

    def register_command_callback(self, callback):
        """
        Adds a callback function (or callable object) to cvallback list to be
        notified when command execution has finished

        Callback signature should be :

            callback(command)

        Where command is the command object itself
        """
        self._command_callbacks.append(callback)

    def remove_command_observer(self, observer):
        """
        Removes a CommandActivatedObserver observer object from observer list
        """
        try:
            self._command_callbacks.remove(observer.command_executed)
        except ValueError:
            pass

    def remove_command_callback(self, callback):
        """
        Deletes a callback function (or callable object) from callback list
        """
        try:
            self._command_observers.remove(callback)
        except ValueError:
            pass

    def clear_command_observers(self):
        """
        Removes all observers object from observers list

        Caution, this command clears both observers and callbacks references
        """
        del self._command_callbacks[:]

    def clear_command_callbacks(self):
        """
        Removes all observers object from observers list

        Caution, this command clears both observers and callbacks references
        """
        del self._command_callbacks[:]

    def notify_command_executed(self):
        """
        Notifies all observers that the command has been executed
        """
        for callback in self._command_callbacks:
            callback(self)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
