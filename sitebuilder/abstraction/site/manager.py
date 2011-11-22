#!/usr/bin/env python

"""
Site configuration management calsses. It supports search, load, create, save
and delete operations.
"""

from sitebuilder.utils.parameters import get_application_context
from sitebuilder.utils.parameters import CONTEXT_NORMAL, CONTEXT_TEST
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.abstraction.site.factory import site_factory
from sitebuilder.utils.driver.test import TestBackendDriver

def get_default_config_data():
    """
    Generates the default site used to initialize internal
    site structures
    """
    return {
        # General attributes
        'general' : {
            'id' : (None, int, 'Id should be a number'),
            'platform' : (SiteDefaultsManager.get_default_platform(),
                          SiteDefaultsManager.get_platforms().keys(),
                          'Unknown platform'),
            'domain' : (SiteDefaultsManager.get_default_domain(),
                        SiteDefaultsManager.get_domains().keys(),
                        'Unknown domain'),
            'name' : ('', '^[\d\w_-]*$', 'Name should be an alphanumeric string'),
            'description' : ('', None),
            'done' : (False, bool),
            },
        # Repository related attriutes
        'repository' : {
            'enabled' : (False, bool),
            'type' : (SiteDefaultsManager.get_default_repository_type(),
                      SiteDefaultsManager.get_repository_types().keys(),
                      'Unsupported RCS type'),
            'name' : ('', '^[\d\w_-]*$', 'Name should be an alphanumeric string or _, without spaces'),
            'done' : (False, bool)
            },
        # Sites related attributes (for each available platform)
        'website' : {
            'enabled' : (False, bool),
            'access' : (SiteDefaultsManager.get_default_site_access(),
                        SiteDefaultsManager.get_site_accesses().keys(),
                        'Unsupported access'),
            'maintenance' : (False, bool),
            'template' : ('standard',
                          SiteDefaultsManager.get_site_templates().keys(),
                          'Unsupported site template'),
            'done' : (False, bool)
            },
        # Databases related attributes (for each available platform)
        'database' : {
            'enabled' : (False, bool),
            'type' : (SiteDefaultsManager.get_default_database_type(),
                      SiteDefaultsManager.get_database_types().keys(),
                      'Unsupported database type'),
            'name' : ('', '^[a-z0-9_]+$', 'Name should be a simple alphanumeric string without spaces'),
            'username' : ('', '^[a-z0-9_]+$', 'Username should be a simple alphanumeric string without spaces'),
            'password' : ('', None),
            'done' : (False, bool)
            },
        }


class SiteConfigurationManager(object):
    """
    Configuration class that handles site read an write operations
    relative to sitebuilder queries.

    It gives informations on queries themselves, but also on certain
    atrributes allowed values such as databases technologies, sites templates
    repositories types available and so on.

    It also manages all the database interractions.

    This class is to be used as a static class and then should never be
    instanciated.
    """
    def __init__(self):
        """
        Since it should be used as a static class, instaciation is forbdden.
        """
        raise NotImplementedError("Oops. Instaciation not allowed")

    def __copy__(self):
        """
        Since it should be used as a static class, cloning is forbdden.
        """
        raise NotImplementedError("Oops. Copy not allowed")

    @staticmethod
    def _get_backend_driver():
        """
        Returns backend driver depending on application execution context
        """
        try:
            return SiteConfigurationManager._backend_driver
        except AttributeError:
            context = get_application_context()

            if context == CONTEXT_NORMAL:
                driver = TestBackendDriver
            elif context == CONTEXT_TEST:
                driver = TestBackendDriver
            else:
                raise RuntimeError("unknonw application context: %s" % context)

            SiteConfigurationManager._backend_driver = driver
            return driver

    @staticmethod
    def get_blank_site():
        """
        Returns a new blank site item.
        """
        return site_factory()

    @staticmethod
    def get_site_by_name(name, domain):
        """
        Loads a site item based on its name and domain. It returns a complete
        and unique site fully defined using backend driver.
        """
        driver = SiteConfigurationManager._get_backend_driver()
        return driver.get_site_by_name(name, domain)

    @staticmethod
    def lookup_host_by_name(name, domain):
        """
        Looks for sites using name and domain as search filter.

        It only loads the subset of sites definition necessary to display
        sites list. Only DNSHost site subset attribute is returned.

        To get fully loaded sites later, use get_site_by_name method.
        """
        driver = SiteConfigurationManager._get_backend_driver()
        return driver.lookup_host_by_name(name, domain)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
