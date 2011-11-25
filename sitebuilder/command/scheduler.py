#!/usr/bin/env python

"""
Command scheduler class
"""

from sitebuilder.application import threadstop
from sitebuilder.utils.parameters import get_application_context
from sitebuilder.utils.parameters import CONTEXT_NORMAL, CONTEXT_TEST
from sitebuilder.utils.driver.test import TestBackendDriver
from sitebuilder.interfaces.command import ICommand
from sitebuilder.interfaces.command import ICommandSubject, ICommandLogged
from sitebuilder.interfaces.command import COMMAND_RUNNING
from sitebuilder.interfaces.command import COMMAND_SUCCESS
from sitebuilder.interfaces.command import COMMAND_ERROR
from sitebuilder.command.log import logger
from Queue import Queue, Empty
from threading import Thread


class CommandScheduler(Thread):
    """
    Command scheduler enques commands and exectes them. Command queue is
    managed in a separate thread to avoid.
    """

    def __init__(self):
        """
        Schedule initialization
        """
        Thread.__init__(self)
        self.backend_driver = None
        self.exec_queue = Queue()

    def get_backend_driver(self):
        """
        Returns backend driver depending on application execution context
        """
        if self.backend_driver is None:
            context = get_application_context()

            if context == CONTEXT_NORMAL:
                driver = TestBackendDriver
            elif context == CONTEXT_TEST:
                driver = TestBackendDriver
            else:
                raise RuntimeError("unknonw application context: %s" % context)

            self.backend_driver = driver

        return self.backend_driver

    def put(self, command):
        """
        Adds a command in the execution queue
        """
        if not ICommand.providedBy(command):
            raise AttributeError("command parameter should be an instance of ICommand")
        self.exec_queue.put(command)

    def run(self):
        """
        Continuously loops on commands and executes them
        """
        while not threadstop.is_set():
            try:
                command = self.exec_queue.get(block=True, timeout=0.1)
            except Empty:
                continue

            print "executing comamnd %s" % str(command)
            command.status = COMMAND_RUNNING

            if ICommandSubject.providedBy(command) and \
               ICommandLogged.providedBy(command):

                # Register logger as command observer for it to be notified
                # when execution has finished
                command.register_command_observer(logger)

            try:
                command.execute(self.get_backend_driver())
                command.status = COMMAND_SUCCESS
            except Exception, e:
                command.status = COMMAND_ERROR
                command.mesg = str(e)
                command.exception = e

            if ICommandSubject.providedBy(command):
                command.notify_command_executed(command)

            command.release()
            self.exec_queue.task_done()
        # End while


if not 'scheduler' in locals():
    scheduler = CommandScheduler()
    scheduler.start()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
