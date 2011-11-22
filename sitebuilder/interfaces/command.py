#!/usr/bin/env python
"""
Command components related interfaces definition
"""

from zope.interface import Interface
from zope.schema import Int, Text, Object

# Command status constants
COMMAND_PENDING = 0
COMMAND_RUNNING = 1
COMMAND_SUCCESS = 2
COMMAND_ERROR   = 3


class ICommand(Interface):
    """
    Command objects are used to perform various operations on storage backends
    """

    # Command status
    status = Int(title="Command status", required=True, default=False)

    # Command result
    result = Object(title="Command result", required=True, default=0)

    # Command return code (Unix command return code equivalent)
    return_code = Int(title="Return code", required=True, default=0)

    # Error message is error occured
    error = Text(title="Error message", required=True, default=0)

    def execute(driver):
        """
        Executes the specific command actions using a backend driver.

        The backend should be fully initialized when passed to execute. For
        instance, if the storage backend uses a RDBMS, the actions should not
        have to initialize the connection tothe database server.
        """

    def wait():
        """
        Waits for the command to be executed.
        """

class ICommandObserver(Interface):
    """
    Observers methods are called on command executed event.
    """

    def command_executed(self, command=None):
        """
        Observer method run on command avtivated event
        """

class ICommandSubject(Interface):
    """
    Subject notify observers on command events
    """

    def register_command_observer(observer):
        """
        Adds a CommandActivatedObserver observer object to observers list
        """

    def remove_command_observer(observer):
        """
        Deletes a CommandActivatedObserver observer object to observers list
        """

    def clear_command_observers():
        """
        Deletes all observers object from observers list
        """

    def notify_command_executed(command):
        """
        Notifies all observers that a data has changed
        """
