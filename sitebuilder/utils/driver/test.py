#!/usr/bin/env python
"""
Test backend driver implementation
"""

from sitebuilder.abstraction.site.factory import site_factory
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
        """
        global _SITES

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
        """
        global _SITES
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
        Adds a site to the site list
        """
        global _SITES
        _SITES.append(site)
