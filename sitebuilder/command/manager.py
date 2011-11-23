#!/usr/bin/env python

"""
Command manager class
"""

from sitebuilder.utils.parameters import get_application_context
from sitebuilder.utils.parameters import CONTEXT_NORMAL, CONTEXT_TEST
from sitebuilder.utils.driver.test import TestBackendDriver
from sitebuilder.interfaces.command import ICommand
from Queue import Queue


class CommandManager(object):
    """
    Command manager enques commands and exectes them. Command queue is managed
    in a separate thread to avoid.
    """
    backend_driver = None
    exec_queue = Queue()

    @staticmethod
    def get_backend_driver():
        """
        Returns backend driver depending on application execution context
        """
        if CommandManager.backend_driver is None:
            context = get_application_context()

            if context == CONTEXT_NORMAL:
                driver = TestBackendDriver
            elif context == CONTEXT_TEST:
                driver = TestBackendDriver
            else:
                raise RuntimeError("unknonw application context: %s" % context)

            CommandManager.backend_driver = driver

        return CommandManager.backend_driver

    @staticmethod
    def put(command):
        """
        Adds a command in the execution queue
        """
        if not ICommand.providedBy(command):
            raise AttributeError("command parameter should be an instance of ICommand")
        CommandManager.exec_queue.put(command)

    @staticmethod
    def run():
        """
        Continuously loops on commands and executes them
        """
        while True:
            command = CommandManager.exec_queue.get(block=True)
            try:
                command.execute(CommandManager.get_backend_driver())
            except:
                pass


if not 'manager' in locals():
    manager = CommandManager
    #manager.run()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
