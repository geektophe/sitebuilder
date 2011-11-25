#!/usr/bin/env python
"""
DNSHost objects related commands
"""

from sitebuilder.interfaces.command import ICommand
from sitebuilder.interfaces.command import ICommandLogged, ICommandSubject
from sitebuilder.interfaces.site import ISite
from sitebuilder.command.base import BaseCommand
from sitebuilder.observer.command import CommandSubject
from zope.interface import implements
import re

class GetSiteByName(BaseCommand):
    """
    Looks for a host using its name and domain
    """
    implements(ICommand)
    name = ""
    domain = ""
    name_re = re.compile(r"^[\w\d_-]+$")
    domain_re = re.compile(r"^[\w\d\._-]+$")

    def __init__(self, name, domain):
        """
        Command initialization.

        Parameters:
            name    Host name
            domain  Domain name
        """
        BaseCommand.__init__(self)

        if not self.name_re.match(name):
            raise AttributeError(r"Invalid host name. Should match /^[\w\d_-]+$/")
        if not self.domain_re.match(domain):
            raise AttributeError(r"Invalid domain name. Should match /^[\w\d\._-]+$/")

        self.name = name
        self.domain = domain

    def execute(self, driver):
        """
        Looks for an host by host and domain name. Result is set a list of
        DNSHost objects.
        """
        result = driver.get_site_by_name(self.name, self.domain)
        self.result = result


class AddSite(BaseCommand, CommandSubject):
    """
    Adds a new site into the backend
    """
    implements(ICommand, ICommandLogged, ICommandSubject)

    site = None

    def __init__(self, site):
        """
        Command initialization.

        Parameters:
            site    Site object to add to backend
        """
        BaseCommand.__init__(self)
        CommandSubject.__init__(self)

        if not ISite.providedBy(site):
            raise AttributeError("Invalid site parametee. Should implement ISite")

        self.site = site

    def execute(self, driver):
        """
        Looks for an host by host and domain name. Result is set a list of
        DNSHost objects.
        """
        name = self.site.dnshost.name
        domain = self.site.dnshost.domain
        hosts = driver.lookup_host_by_name(name, domain)

        if len(hosts):
            raise ValueError("Site %s.%s already exists" % (name, domain))

        driver.add_site(self.site)
