#!/usr/bin/env python
"""
DNSHost objects related commands
"""

from sitebuilder.interface.command import ICommand
from sitebuilder.command.base import BaseCommand
from zope.interface import implements
import threading

class LookupHostByName(BaseCommand):
    """
    Looks for a host using its name and domain
    """
    implements(ICommand)
    name = ""
    domain = ""

    def __init__(self, name, domain):
        """
        Command initialization.

        Parameters:
            name    Host name (may use wilcards characher *)
            domain  Domain name (may use wilcards characher *)
        """
        self.name = name
        self.domain = domain
        self.executed = threading.Event()

    def wait(self, timeout=None):
        """
        Waits for command to be executed
        """
        self.executed.wait()

    def excecute(self, driver):
        """
        Looks for an host by host and domain name. Result is set a list of
        DNSHost objects.
        """
