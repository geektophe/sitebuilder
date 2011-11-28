#!/usr/bin/env python
"""
Log manager classes
"""

from sitebuilder.application import threadstop
from sitebuilder.interfaces.command import ICommandObserver
from sitebuilder.interfaces.command import COMMAND_SUCCESS, COMMAND_ERROR
from zope.interface import implements
from Queue import Queue, Empty
from threading import Thread
import sys

# Module level log queue
log_queue = Queue()

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

    def command_executed(self, command):
        """
        Adds a command into the log queue
        """
        log_queue.put(command)

    def run(self):
        """
        Continuously loops on commands and log messages
        """
        while not threadstop.is_set():
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


logger = LogManager()
logger.start()
