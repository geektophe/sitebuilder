#!/usr/bin/env python
"""
Base command that command implementations may subclass
"""

from zope.schema.fieldproperty import FieldProperty
from sitebuilder.interfaces.command import ICommand, COMMAND_PENDING


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

    def __init__(self):
        self.state = COMMAND_PENDING
