#!/usr/bin/env python
"""
Test backend driver implementation
"""

from sitebuilder.abstraction.site.factory import site_factory
from sitebuilder.exception import BackendError
from copy import deepcopy
import re


def get_test_site(name):
    """
    Generates the default siteuration used to initialize internal
    site structures
    """
    site = site_factory()

    site.dnshost.name = name
    site.dnshost.description = 'desc %s' % name

    site.repository.enabled = True
    site.repository.done = True

    site.website.enabled = True
    site.website.maintenance = True
    site.website.done = True

    site.database.enabled = True
    site.database.name = 'db_%s' % name
    site.database.username = 'username_%s' % name
    site.database.password = 'password_%s' % name
    site.database.done = True

    return site


# Module level site list
_SITES = [ get_test_site("name%d" % num) for num in range(10) ]


class TestBackendDriver(object):
    """
    Test implementation backend driver
    """

    @staticmethod
    def get_site_by_name(name, domain):
        """
        Loads a site item based on its name and domain. It returns a complete
        and unique site fully defined using backend driver.

        Note that if several hosts match the couple name/domain, only the
        first occurence is returned, leading to an undertermined result.

        >>> from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
        >>> site = TestBackendDriver.get_site_by_name('name0', SiteDefaultsManager.get_default_domain())
        >>> site.dnshost.name
        u'name0'
        >>> site.dnshost.domain == SiteDefaultsManager.get_default_domain()
        True
        """
        for site in _SITES:
            dnshost = site.dnshost
            if dnshost.name.lower() == name.lower() and \
               dnshost.domain.lower() == domain.lower():
                return deepcopy(site)

        return None

    @staticmethod
    def lookup_host_by_name(name, domain):
        """
        Looks for sites using name and domain as search filter.

        It only loads the subset of sites definition necessary to display
        sites list. Only DNSHost site subset attribute is returned.

        To get fully loaded sites later, use get_site_by_name method.

        Name and domain parameters may use wilcard characters (*).

        >>> hosts = TestBackendDriver.lookup_host_by_name('*', '*')
        >>> len(hosts) == len(_SITES)
        True
        >>> found = [ False for i in range(len(hosts)) ]
        >>> i = 0
        >>> for host in hosts:
        ...     for dbsite in _SITES:
        ...         if dbsite.dnshost.name == host.name and dbsite.dnshost.domain == host.domain:
        ...             found[i] = True
        ...     i += 1
        ...
        >>> test = [ True for i in range(len(_SITES)) ]
        >>> test == found
        True
        """
        sites = []

        name_re = re.compile("^%s$" % name.replace('*', '.*'))
        domain_re = re.compile("^%s$" % domain.replace('*', '.*'))

        for site in _SITES:
            dnshost = site.dnshost
            if name_re.match(dnshost.name) and domain_re.match(dnshost.domain):
                sites.append(deepcopy(dnshost))

        return sites

    @staticmethod
    def add_site(site):
        """
        Adds a site into the site list

        >>> initlen = len(_SITES)
        >>> site = site_factory()
        >>> site.name = u'test'
        >>> TestBackendDriver.add_site(site)
        >>> len(_SITES) == (initlen + 1)
        True
        >>> found = False
        >>> for dbsite in _SITES:
        ...     if dbsite.dnshost.name == site.dnshost.name and dbsite.dnshost.domain == site.dnshost.domain:
        ...         found = True
        ...
        >>> found
        True
        """
        name = site.dnshost.name
        domain = site.dnshost.domain

        hosts = TestBackendDriver.lookup_host_by_name(name, domain)

        if len(hosts):
            mesg = "Site %s.%s already exists" % (name, domain)
            raise BackendError(mesg)

        dbsite = site_factory()

        dbsite.dnshost.name = site.dnshost.name
        dbsite.dnshost.domain = site.dnshost.domain
        dbsite.dnshost.description = site.dnshost.description
        dbsite.dnshost.platform = site.dnshost.platform
        dbsite.dnshost.done = site.dnshost.done

        dbsite.website.enabled = site.website.enabled
        dbsite.website.maintenance = site.website.maintenance
        dbsite.website.access = site.website.access
        dbsite.website.template = site.website.template
        dbsite.website.done = site.website.done

        dbsite.repository.enabled = site.repository.enabled
        dbsite.repository.name = site.repository.name
        dbsite.repository.type = site.repository.type
        dbsite.repository.done = site.repository.done

        dbsite.database.enabled = site.database.enabled
        dbsite.database.name = site.database.name
        dbsite.database.username = site.database.username
        dbsite.database.password = site.database.password
        dbsite.database.type = site.database.type
        dbsite.database.done = site.database.done

        _SITES.append(dbsite)


    @staticmethod
    def update_site(site):
        """
        Edits a site into the site list and applies site object changes

        >>> from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
        >>> site = TestBackendDriver.get_site_by_name('name0', SiteDefaultsManager.get_default_domain())
        >>> site.dnshost.description = u'a test description'
        >>> TestBackendDriver.update_site(site)
        >>> site = TestBackendDriver.get_site_by_name('name0', SiteDefaultsManager.get_default_domain())
        >>> site.dnshost.description
        u'a test description'

        Name or domain shouldn't be modifiable

        >>> site = TestBackendDriver.get_site_by_name('name0', SiteDefaultsManager.get_default_domain())
        >>> site.dnshost.name = u'atestname'
        >>> TestBackendDriver.update_site(site)
        Traceback (most recent call last):
            ...
        BackendError: Unknown site atestname.bpinet.com
        >>> hosts = TestBackendDriver.lookup_host_by_name('atestname', '*')
        >>> hosts
        []
        >>> hosts = TestBackendDriver.lookup_host_by_name('name0', '*')
        >>> hosts[0].name
        u'name0'
        """
        name = site.dnshost.name
        domain = site.dnshost.domain

        hosts = TestBackendDriver.lookup_host_by_name(name, domain)

        if not len(hosts):
            mesg = "Unknown site %s.%s" % (name, domain)
            raise BackendError(mesg)

        if len(hosts) > 1:
            mesg = "Several sites named %s.%s found" % (name, domain)
            raise BackendError(mesg)

        for dbsite in _SITES:
            dnshost = dbsite.dnshost
            if dnshost.name.lower() == name.lower() and \
               dnshost.domain.lower() == domain.lower():
                break

        print "updating site %s.%s" % (dbsite.dnshost.name, dbsite.dnshost.domain)
        # Apply changes. No chnage on name nor domain allowed
        dbsite.dnshost.description = site.dnshost.description
        dbsite.dnshost.platform = site.dnshost.platform
        dbsite.dnshost.domain = site.dnshost.domain
        dbsite.dnshost.done = site.dnshost.done

        dbsite.website.enabled = site.website.enabled
        dbsite.website.maintenance = site.website.maintenance
        dbsite.website.access = site.website.access
        dbsite.website.template = site.website.template
        dbsite.website.done = site.website.done

        dbsite.repository.enabled = site.repository.enabled
        dbsite.repository.name = site.repository.name
        dbsite.repository.type = site.repository.type
        dbsite.repository.done = site.repository.done

        dbsite.database.enabled = site.database.enabled
        dbsite.database.name = site.database.name
        dbsite.database.username = site.database.username
        dbsite.database.password = site.database.password
        dbsite.database.type = site.database.type
        dbsite.database.done = site.database.done

    @staticmethod
    def delete_site(name, domain):
        """
        Edits a site into the site list and applies site object changes

        >>> from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
        >>> initlen = len(_SITES)
        >>> TestBackendDriver.delete_site('name1', SiteDefaultsManager.get_default_domain())
        >>> len(_SITES) == (initlen - 1)
        True
        >>> hosts = TestBackendDriver.lookup_host_by_name('name1', '*')
        >>> hosts
        []
        """
        hosts = TestBackendDriver.lookup_host_by_name(name, domain)

        if not len(hosts):
            mesg = "Site %s.%s already exists" % (name, domain)
            raise BackendError(mesg)

        i = 0
        for site in _SITES:
            dnshost = site.dnshost
            if dnshost.name.lower() == name.lower() and \
               dnshost.domain.lower() == domain.lower():
                # Deletes site
                del(_SITES[i])

            i += 1


if __name__ == "__main__":
    import doctest
    doctest.testmod()
