#!/usr/bin/env python
"""
Command components related interfaces definition
"""

from zope.interface import Interface, Attribute
from zope.schema import Int

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
    status = Int(title=u"Command status", required=True, default=False)

    # Command return code (Unix command return code equivalent)
    return_code = Int(title=u"Return code", required=True, default=0)

    # Command result
    result = Attribute(u"Command result")

    # Error message is error occured
    mesg = Attribute(u"Success or error message")

    def execute(driver):
        """
        Executes the specific command actions using a backend driver.

        The backend should be fully initialized when passed to execute. For
        instance, if the storage backend uses a RDBMS, the actions should not
        have to initialize the connection tothe database server.
        """

    def wait(timeout=None):
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


class ICommandLogged(Interface):
    """
    Marker interface a command should implement for its result to be logged
    in log subsystem
    """
