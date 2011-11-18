#!/usr/bin/env python

"""
Site configuration management calsses. It supports search, load, create, save
and delete operations.
"""

from sitebuilder.utils.parameters import get_application_context
from sitebuilder.utils.parameters import CONTEXT_NORMAL, CONTEXT_TEST
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.abstraction.site.object import Site

def get_default_config_data():
    """
    Generates the default configuration used to initialize internal
    configuration structures
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


def get_default_config_object():
    """
    Generates the default configuration used to initialize internal
    configuration structures
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


def get_test_configuration(name, domain):
    """
    Generates the default configuration used to initialize internal
    configuration structures
    """
    config = SiteConfigurationManager.get_blank_configuration()

    config.dnshost.name = name
    config.dnshost.description = 'desc_%s' % name

    config.repository.enabled = True
    config.repository.done = True

    config.website.enabled = True
    config.website.maintenance = True
    config.website.done = True

    config.database.enabled = True
    config.database.name = 'db_%s' % name
    config.database.username = 'username_%s' % name
    config.database.password = 'password_%s' % name
    config.database.done = True

    return config


class SiteConfigurationManager(object):
    """
    Configuration class that handles configuration read an write operations
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
    def get_blank_configuration():
        """
        Returns a new blank configuration item.
        """
        return Site()

    @staticmethod
    def get_test_configuration(name, domain):
        """
        Returns a new blank configuration item.
        """
        return get_test_configuration(name, None)

    @staticmethod
    def get_configuration_by_name(name, domain):
        """
        Loads a configuration item based on its id.
        """
        context = get_application_context()

        if context == CONTEXT_NORMAL:
            return SiteConfigurationManager.get_test_configuration_by_name(
                    name, domain)
        elif context == CONTEXT_TEST:
            return SiteConfigurationManager.get_real_configuration_by_name(
                    name, domain)
        else:
            return None

    @staticmethod
    def get_test_configuration_by_name(name, domain):
        """
        If test context is enabled, returns a test configuration set.
        """
        return get_test_configuration(name, domain)

    @staticmethod
    def get_real_configuration_by_name(name, domain):
        """
        If test context is enabled, returns the real configuration set.
        """
        return get_test_configuration(name, domain)

    @staticmethod
    def get_configuration_all():
        """
        Loads all configureation items contained in the configuration
        repository
        """
        context = get_application_context()

        if context == 'normal':
            return SiteConfigurationManager.get_test_configuration_all()
        elif context == 'test':
            return SiteConfigurationManager.get_real_configuration_all()
        else:
            return None

    @staticmethod
    def get_test_configuration_all():
        """
        Returns a list of test configuration set
        """
        configurations = []

        for identifier in range(10):
            configurations.append(
                get_test_configuration("name%s" % identifier, None))

        return configurations

    @staticmethod
    def get_real_configuration_all():
        """
        Returns the list of all configuration set contained in the
        configuration repository
        """
        return SiteConfigurationManager.get_test_configuration_all()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
