#!/usr/bin/env python
"""
DNSHost objects related commands
"""

from sitebuilder.command.interface import ICommand
from sitebuilder.observer.command import ICommandSubject, CommandSubject
from sitebuilder.command.base import BaseCommand
from zope.interface import implements
from threading import Event
import re

class LookupHostByName(BaseCommand, CommandSubject):
    """
    Looks for a host using its name and domain
    """
    implements(ICommand, ICommandSubject)
    description = "Host lookup by name"
    name = ""
    domain = ""
    name_re = re.compile(r"^[\w\d\*_-]+$")
    domain_re = re.compile(r"^[\w\d\*\._-]+$")

    def __init__(self, name, domain):
        """
        Command initialization.

        Parameters:
            name    Host name (may use wilcards characher *)
            domain  Domain name (may use wilcards characher *)
        """
        BaseCommand.__init__(self)
        CommandSubject.__init__(self)

        # Parameters check
        if not self.name_re.match(name):
            raise AttributeError("Invalid host name. Should match /^[\w\d\*_-]+$/")
        if not self.domain_re.match(domain):
            raise AttributeError("Invalid domain name. Should match /^^[\w\d\*\._-]+$/")

        self.name = name
        self.domain = domain
        self.executed = Event()

    def execute(self, driver):
        """
        Looks for an host by host and domain name. Result is set a list of
        DNSHost objects.
        """
        result = driver.lookup_host_by_name(self.name, self.domain)
        self.result = result
