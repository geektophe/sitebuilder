#!/usr/bin/env python
"""
Log manager classes
"""

from sitebuilder.interfaces.command import ICommandObserver
from sitebuilder.interfaces.command import COMMAND_SUCCESS, COMMAND_ERROR
from zope.interface import implements
from threading import Thread
from Queue import Queue

class LogManager(object):
    """
    Logs commands into log system
    """
    implements(ICommandObserver)

    def __init__(self):
        """
        Logger initialization
        """
        #Thread.__init__(self)
        self.log_queue = Queue()

    def command_executed(self, command):
        """
        Adds a command into the log queue
        """
        self.log_queue.put(command)
        #TODO: find a way to exit threads cleanly
        self.run()

    def run(self):
        """
        Continuously loops on commands and log messages
        """
        i = 0

        while i < 1:
            command = self.log_queue.get(block=True)

            if command.status == COMMAND_SUCCESS:
                print "%s: success: %s" % (str(type(command)), command.result)
            elif command.status == COMMAND_ERROR:
                print "%s: error: %s" % (str(type(command)), command.result)
            else:
                print "Unknown command status"
            i += 1
        # End while


if not 'logger' in locals():
    logger = LogManager()
    #logger.start()
