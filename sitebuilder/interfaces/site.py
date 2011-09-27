#!/usr/bin/env python
"""
Site components related interfaces definition
"""

from zope.interface import Interface


class ISite(Interface):
    """
    Interface describing a site object
    """

class IDNSHost(Interface):
    """
    Interface describing site general settings
    """

class IWebsite(Interface):
    """
    Interface describing website related settings
    """

class IDatabase(Interface):
    """
    Interface describing database related settings
    """

class IRCSRepository(Interface):
    """
    Interface describing RCS repository related settings
    """
