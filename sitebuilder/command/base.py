#!/usr/bin/env python
"""
Base command that command implementations may subclass
"""

from zope.schema.dieldproperty import FieldProperty
from sitebuilder.interface.command import ICommand


#TODO: write a decorator that checks execute parameter type

class BaseCommand(object):
    """
    Base command class.

    Base subclasses should implement execute and wait methods
    """
    state = FieldProperty(ICommand['state'])
    return_code = FieldProperty(ICommand['return_code'])
    error = None
    result = None
