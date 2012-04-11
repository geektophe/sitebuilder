#!/usr/bin/env python
"""
DNSHost objects related commands
"""

from sitebuilder.command.interface import ICommand, ICommandLogged
from sitebuilder.observer.command import ICommandSubject, CommandSubject
from sitebuilder.abstraction.interface import ISite
from sitebuilder.command.base import BaseCommand
from zope.interface import implements
import re

class GetSiteByName(BaseCommand, CommandSubject):
    """
    Looks for a host using its name and domain
    """
    implements(ICommand, ICommandSubject)
    description = "Site lookup by name"
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
        CommandSubject.__init__(self)

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
    implements(ICommand, ICommandSubject, ICommandLogged)
    description = "Add site"

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
        Executes command
        """
        name = self.site.dnshost.name
        domain = self.site.dnshost.domain
        hosts = driver.lookup_host_by_name(name, domain)

        if len(hosts):
            self.mesg = "Site %s.%s already exists" % (name, domain)
            raise ValueError(self.mesg)

        driver.add_site(self.site)
        self.mesg = "Site %s.%s successfully added" % (name, domain)


class UpdateSite(BaseCommand, CommandSubject):
    """
    Edits a new site into the backend applying the values from site object
    """
    implements(ICommand, ICommandSubject, ICommandLogged)
    description = "Update site"

    site = None

    def __init__(self, site):
        """
        Command initialization.

        Parameters:
            site    Site object to apply attributes to backend
        """
        BaseCommand.__init__(self)
        CommandSubject.__init__(self)

        if not ISite.providedBy(site):
            raise AttributeError("Invalid site parametee. Should implement ISite")

        self.site = site

    def execute(self, driver):
        """
        Executes command
        """
        name = self.site.dnshost.name
        domain = self.site.dnshost.domain
        hosts = driver.lookup_host_by_name(name, domain)

        if not len(hosts):
            self.mesg = "Unknown site %s.%s" % (name, domain)
            raise ValueError(self.mesg)

        if len(hosts) > 1:
            self.mesg = "Several sites named %s.%s found" % (name, domain)
            raise ValueError(self.mesg)

        driver.update_site(self.site)
        self.mesg = "Site %s.%s successfully updated" % (name, domain)


class DeleteSite(BaseCommand, CommandSubject):
    """
    Deletes a site using its name and domain
    """
    implements(ICommand, ICommandSubject, ICommandLogged)
    description = "Delete site"
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
        CommandSubject.__init__(self)

        if not self.name_re.match(name):
            raise AttributeError(r"Invalid host name. Should match /^[\w\d_-]+$/")
        if not self.domain_re.match(domain):
            raise AttributeError(r"Invalid domain name. Should match /^[\w\d\._-]+$/")

        self.name = name
        self.domain = domain

    def execute(self, driver):
        """
        Tells backend driver to delete site idetified by name and domain
        parameter
        """
        hosts = driver.lookup_host_by_name(self.name, self.domain)

        if not len(hosts):
            self.mesg = "Unknown site %s.%s" % (self.name, self.domain)
            raise ValueError(self.mesg)

        if len(hosts) > 1:
            self.mesg = "Several sites named %s.%s found" % (self.name, self.domain)
            raise ValueError(self.mesg)

        driver.delete_site(self.name, self.domain)
        self.mesg = "Site %s.%s successfully deleted" % (self.name, self.domain)
