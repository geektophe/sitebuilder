#!/usr/bin/env python
"""
DNSHost objects related commands
"""

from sitebuilder.interfaces.command import ICommand
from sitebuilder.command.base import BaseCommand
from zope.interface import implements
from threading import Event
import re

class GetSiteByName(BaseCommand):
    """
    Looks for a host using its name and domain
    """
    implements(ICommand)
    name = ""
    domain = ""
    name_re = re.compile("^[\w_-]+$")
    domain_re = re.compile("^[\w\._-]+$")

    def __init__(self, name, domain):
        """
        Command initialization.

        Parameters:
            name    Host name
            domain  Domain name
        """
        BaseCommand.__init__(self)

        if not self.name_re.match(name):
            raise AttributeError("Invalid host name. Should match /^[\w_-]+$/")
        if not self.name_re.match(name):
            raise AttributeError("Invalid domain name. Should match /^[\w\._-]+$/")

        self.name = name
        self.domain = domain
        self.executed = Event()

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
        result = driver.get_site_by_name(self.name, self.domain)
        self.result = result
        self.executed.set()
