#!/usr/bin/env python
"""
Base command that command implementations may subclass
"""

from zope.schema.fieldproperty import FieldProperty
from sitebuilder.command.interface import ICommand, COMMAND_PENDING
from threading import Event


#TODO: write a decorator that checks execute parameter type

class BaseCommand(object):
    """
    Base command class.

    Base subclasses should implement execute and wait methods
    """
    status = FieldProperty(ICommand['status'])
    return_code = FieldProperty(ICommand['return_code'])
    mesg = None
    result = None
    excption = None

    def __init__(self):
        self.state = COMMAND_PENDING
        self._lock = Event()

    def wait(self, timeout=None):
        """
        Waits for command to be executed
        """
        self._lock.wait(timeout)

    def release(self):
        """
        Releases execution lock
        """
        self._lock.set()
