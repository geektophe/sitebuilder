#!/usr/bin/env python
"""
Command components related interfaces definition
"""

from zope.interface import Interface, Attribute
from zope.schema import Int, TextLine

# Command status constants
COMMAND_PENDING = 0
COMMAND_RUNNING = 1
COMMAND_SUCCESS = 2
COMMAND_ERROR   = 3


class ICommand(Interface):
    """
    Command objects are used to perform various operations on storage backends
    """

    # String giving succinct command description
    description = TextLine(title=u"Short commande description", required=True, default=u"")

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

    # Error message is error occured
    traceback = Attribute(u"Exception traceback")

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
