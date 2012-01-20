#!/usr/bin/env python

"""
Command scheduler class
"""

from sitebuilder.utils.parameters import get_application_context
from sitebuilder.utils.parameters import CONTEXT_NORMAL, CONTEXT_TEST
from sitebuilder.utils.driver.test import TestBackendDriver
from sitebuilder.interfaces.command import ICommand
from sitebuilder.interfaces.command import ICommandSubject, ICommandLogged
from sitebuilder.interfaces.command import COMMAND_RUNNING
from sitebuilder.interfaces.command import COMMAND_SUCCESS
from sitebuilder.interfaces.command import COMMAND_ERROR
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
notifier = None


def start():
    """
    Initialises scheduler and notifier instances and start threads
    """
    global scheduler
    global notifier

    if scheduler is None:
        # Command execution scheduler module level instance
        scheduler = CommandExecScheduler()
        scheduler.start()

        # Commend notifications scheduler module level instance
        notifier = CommandNotificationScheduler()
        notifier.start()
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
    notifier.join()
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

            if ICommandSubject.providedBy(command) and \
               ICommandLogged.providedBy(command):
                # Register logger as command observer for it to be notified
                # when execution has finished
                command.register_command_callback(log_enqueue_command)

            command.status = COMMAND_RUNNING

            try:
                command.execute(self.get_backend_driver())
                command.status = COMMAND_SUCCESS
            except Exception, e:
                command.status = COMMAND_ERROR
                command.exception = e
                command.traceback = format_exc(e)

            command.release()

            if ICommandSubject.providedBy(command):
                notify_queue.put_nowait(command)

            exec_queue.task_done()
        # End while


class CommandNotificationScheduler(Thread):
    """
    Command scheduler enques commands and exectes them. Command queue is
    managed in a separate thread to avoid.
    """

    def __init__(self):
        """
        Schedule initialization
        """
        Thread.__init__(self)
        self.name = "CommandNotificationScheduler"
        self.daemon = True

    def run(self):
        """
        Continuously loops on commands and notify them
        """
        while not thread_stop.is_set():
            try:
                command = notify_queue.get(timeout=0.1)
            except Empty:
                continue

            if ICommandSubject.providedBy(command):
                # Sends back notification method execution in main thread
                # Very important with PyGTK !
                gobject.idle_add(command.notify_command_executed)

            notify_queue.task_done()
        # End while



if __name__ == "__main__":
    import doctest
    doctest.testmod()
