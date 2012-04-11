#!/usr/bin/env python
"""
Log manager classes
"""

from sitebuilder.command.interface import ICommand, ICommandObserver
from sitebuilder.command.interface import COMMAND_SUCCESS, COMMAND_ERROR
from zope.interface import implements
from Queue import Queue, Empty
from warnings import warn
from threading import Thread, Event
import sys

# Module level log queue
log_queue = Queue()
thread_stop = Event()
logger = None


def start():
    """
    Initialises logger instance and start threads
    """
    global logger

    if logger is None:
        logger = LogManager()
        logger.start()
    else:
        warn("'start' called on an already initialized instance")


def stop():
    """
    Stops logger instances
    """
    thread_stop.set()


def enqueue_command(command):
    """
    Adds a command to the execution queue
    """
    if logger is None:
        warn("enqued command but logger has not been initialized. " +
             "use 'start' function to initialize it")

    if not ICommand.providedBy(command):
        raise AttributeError("command parameter should be an instance of ICommand")

    # Adds command to execution queue
    log_queue.put(command)


class LogManager(Thread):
    """
    Logs commands into log system
    """
    implements(ICommandObserver)

    name = "LogManager"

    def __init__(self):
        """
        Logger initialization
        """
        Thread.__init__(self)

    def run(self):
        """
        Continuously loops on commands and log messages
        """
        while not thread_stop.is_set():
            try:
                command = log_queue.get(timeout=0.1)
            except Empty:
                continue

            if command.status == COMMAND_SUCCESS:
                print "%s: success: %s" % (str(type(command)), command.result)
            elif command.status == COMMAND_ERROR:
                print "%s: error: %s" % (str(type(command)), command.mesg)
            else:
                print "Unknown command status: %s" % command.status

            sys.stdout.flush()
            log_queue.task_done()
        # End while
