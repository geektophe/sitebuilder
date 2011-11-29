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

    # Error message is error occured
    exception = Attribute(u"Exception object risen if error occured")

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

    def release():
        """
        Releases a locked command
        """


class ICommandObserver(Interface):
    """
    Observers methods are called on command executed event.
    """

    def command_executed(self, command):
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


class ICommandLogged(Interface):
    """
    Marker interface a command should implement for its result to be logged
    in log subsystem
    """
