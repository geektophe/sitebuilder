#!/usr/bin/env python

"""
Command scheduler class
"""

from sitebuilder.utils.parameters import get_application_context
from sitebuilder.utils.parameters import CONTEXT_NORMAL, CONTEXT_TEST
from sitebuilder.utils.driver.test import TestBackendDriver
from sitebuilder.command.interface import ICommand, ICommandLogged
from sitebuilder.command.interface import COMMAND_RUNNING
from sitebuilder.command.interface import COMMAND_SUCCESS
from sitebuilder.command.interface import COMMAND_ERROR
from sitebuilder.event.events import CommandExecEvent
from sitebuilder.command.log import enqueue_command as log_enqueue_command
from traceback import format_exc
from Queue import Queue, Empty
from threading import Thread, Event
from warnings import warn
import gobject


# Module level execution queue
exec_queue = Queue()
notify_queue = Queue()
thread_stop = Event()
scheduler = None


def start():
    """
    Initialises scheduler and notifier instances and start threads
    """
    global scheduler

    if scheduler is None:
        # Command execution scheduler module level instance
        scheduler = CommandExecScheduler()
        scheduler.start()
    else:
        warn("'start' called on an already initialized instance")


def stop():
    """
    Stops scheduler and notifier instances
    """
    global scheduler
    global notifier

    thread_stop.set()
    scheduler.join()
    scheduler = None
    notifier = None


def enqueue_command(command):
    """
    Adds a command to the execution queue
    """
    if scheduler is None:
        warn("enqued command but scheduler has not been initialized. " +
             "use 'start' function to initialize it")

    if not ICommand.providedBy(command):
        raise AttributeError("command parameter should be an instance of ICommand")

    # Adds command to execution queue
    exec_queue.put(command)


class CommandExecScheduler(Thread):
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
        self.name = "CommandExecScheduler"
        self.daemon = True

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

    def run(self):
        """
        Continuously loops on commands and executes them
        """
        while not thread_stop.is_set():
            try:
                command = exec_queue.get(timeout=0.1)
            except Empty:
                continue

            if ICommandLogged.providedBy(command):
                # Register logger as command observer for it to be notified
                # when execution has finished
                command.get_event_bus().subscribe(CommandExecEvent,
                                                  self.log_command)

            command.status = COMMAND_RUNNING

            try:
                command.execute(self.get_backend_driver())
                command.status = COMMAND_SUCCESS
            except Exception, e:
                command.status = COMMAND_ERROR
                command.exception = e
                command.traceback = format_exc(e)

            command.release()
            exec_queue.task_done()

            # Notifies followers that the command has been executed
            gobject.idle_add(
                lambda: command.get_event_bus().publish(CommandExecEvent(command)))
        # End while

    def log_command(self, event):
        """
        Appends a command to the log queue
        """
        log_enqueue_command(event.source)

    def notify_command_executed(self):
        """
        Publishes an event to indacate that the commande has been executed.
        """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
