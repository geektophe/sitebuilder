#!/usr/bin/env python
"""
Observer classes associated with the Command events
"""

from zope.interface import implements
from sitebuilder.interfaces.command import ICommand, ICommandSubject, ICommandObserver


class CommandSubject(object):
    """
    Subject base class to handle Command events

    >>> from zope.schema.fieldproperty import FieldProperty
    >>> class TestCommand(CommandSubject):
    ...     implements(ICommand, ICommandObserver)
    ...     status = FieldProperty(ICommand['status'])
    ...     result = FieldProperty(ICommand['result'])
    ...     return_code = FieldProperty(ICommand['return_code'])
    ...     error = FieldProperty(ICommand['error'])
    ...     def wait(self, timeout=None):
    ...         pass
    ...     def execute(self, driver):
    ...         self.notify_command_executed(self)
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

    Notified object should implement ICommand. If not so, an exception
    should be risen
    >>> command.notify_command_executed('fake')
    Traceback (most recent call last):
        ...
    AttributeError: command parameter should implement ICommand
    """

    implements(ICommandSubject)

    def __init__(self):
        """
        Subject initialization
        """
        self._command_observers = []

    def register_command_observer(self, observer):
        """
        Adds a CommandObserver observer object to observers list
        """
        if not ICommandObserver.providedBy(observer):
            raise AttributeError("Observer should implement ICommandObserver")
        self._command_observers.append(observer)

    def remove_command_observer(self, observer):
        """
        Deletes a CommandObserver observer object to observers list
        """
        try:
            self._command_observers.remove(observer)
        except ValueError:
            pass

    def clear_command_observers(self):
        """
        Deletes all AddCommandListener observers object from observers
        list
        """
        del self._command_observers[:]

    def notify_command_executed(self, command=None):
        """
        Notifies all observers that that an command has been executed
        """
        if command is not None and not ICommand.providedBy(command):
            raise AttributeError("command parameter should implement ICommand")

        for observer in self._command_observers:
            observer.command_executed(command)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
