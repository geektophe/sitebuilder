#!/usr/bin/env python

"""
Configuration related classes
"""

from sitebuilder.utils.parameters import get_application_context
from sitebuilder.utils.attribute import AttributeSet


def get_default_config_data():
    """
    Generates the default configuration used to initialize internal
    configuration structures
    """
    return {
        # General attributes
        'general' : {
            'id' : (None, int, 'Id should be a number'),
            'name' : ('', '^[\d\w\s_-]*$', 'Name should be an alphanumeric string'),
            'description' : ('', '^[\d\w\s_-]*$', 'Reference should be an alphanumeric string')
            },
        # Repository related attriutes
        'repository' : {
            'enabled' : (False, bool),
            'type' : ('svn', ConfigurationManager.get_repository_types().keys(), 'Unsupported RCS type'),
            'name' : ('', '^[\d\w_-]*$', 'Name should be an alphanumeric string or _, without spaces'),
            'done' : (False, bool)
            },
        # Sites related attributes (for each available platform)
        'sites' : {
            'prod' : {
                'enabled' : (False, bool),
                'proxied' : (False, bool),
                'maintenance' : (False, bool),
                'done' : (False, bool),
                'template' : ('standard', ConfigurationManager.get_site_templates().keys(), 'Unsupported site template'),
                'domain' : ('bpinet.com', ConfigurationManager.get_site_domains().keys(), 'Unknown domain'),
                'name' : ('__DEFAULT__', '^([a-z0-9_-]+|__DEFAULT__)$', 'Name should be a simple alphanumeric string without spaces')
                },
            'test' : {
                'enabled' : (False, bool),
                'proxied' : (False, bool),
                'maintenance' : (False, bool),
                'done' : (False, bool),
                'template' : ('standard', ConfigurationManager.get_site_templates().keys(), 'Unsupported site template'),
                'domain' : ('bpinet.com', ConfigurationManager.get_site_domains().keys(), 'Unknown domain'),
                'name' : ('__DEFAULT__', '^([a-z0-9_-]+|__DEFAULT__)$', 'Name should be a simple alphanumeric string without spaces')
                },
            'dev' : {
                'enabled' : (False, bool),
                'maintenance' : (False, bool),
                'done' : (False, bool),
                'template' : ('standard', ConfigurationManager.get_site_templates().keys(), 'Unsupported site template'),
                'domain' : ('bpinet.com', ConfigurationManager.get_site_domains().keys(), 'Unknown domain'),
                'name' : ('__DEFAULT__', '^([a-z0-9_-]+|__DEFAULT__)$', 'Name should be a simple alphanumeric string without spaces')
                },
            },
        # Databases related attributes (for each available platform)
        'databases' : {
            'prod' : {
                'enabled' : (False, bool),
                'done' : (False, bool),
                'type' : ('mysql', ConfigurationManager.get_database_types().keys(), 'Unsupported database type'),
                'name' : ('', '^[a-z0-9_]+$', 'Name should be a simple alphanumeric string without spaces'),
                'username' : ('', '^[a-z0-9_]+$', 'Username should be a simple alphanumeric string without spaces'),
                'password' : ('', None)
                },
            'test' : {
                'enabled' : (False, bool),
                'done' : (False, bool),
                'type' : ('mysql', ConfigurationManager.get_database_types().keys(), 'Unsupported database type'),
                'name' : ('', '^[a-z0-9_]+$', 'Name should be a simple alphanumeric string without spaces'),
                'username' : ('', '^[a-z0-9_]+$', 'Username should be a simple alphanumeric string without spaces'),
                'password' : ('', None)
                },
            'dev' : {
                'enabled' : (False, bool),
                'done' : (False, bool),
                'type' : ('mysql', ConfigurationManager.get_database_types().keys(), 'Unsupported database type'),
                'name' : ('', '^[a-z0-9_]+$', 'Name should be a simple alphanumeric string without spaces'),
                'username' : ('', '^[a-z0-9_]+$', 'Username should be a simple alphanumeric string without spaces'),
                'password' : ('', None)
                },
            }
        }


def get_test_configuration(config_id):
    """
    Generates the default configuration used to initialize internal
    configuration structures
    """
    config = ConfigurationManager.get_blank_configuration()

    general = config.get_attribute('general')
    general.get_attribute('id').set_value(config_id)
    general.get_attribute('name').set_value('name%d' % config_id)
    general.get_attribute('description').set_value('desc%d' % config_id)

    repository = config.get_attribute('repository')
    repository.get_attribute('enabled').set_value(True)
    repository.get_attribute('name').set_value('repo%d' % config_id)
    repository.get_attribute('done').set_value(False)

    i = 0
    sites = config.get_attribute('sites')

    for platform in sites.get_attribute_names():
        site = sites.get_attribute(platform)

        if i % 2 == 0:
            site.get_attribute('enabled').set_value(True)

            if 'proxied' in site.get_attribute_names():
                site.get_attribute('proxied').set_value(True)

            site.get_attribute('maintenance').set_value(True)
            site.get_attribute('done').set_value(True)
            site.get_attribute('name').set_value('%s_site' % platform)

        else:
            site.get_attribute('enabled').set_value(False)

            if 'proxied' in site.get_attribute_names():
                site.get_attribute('proxied').set_value(False)

            site.get_attribute('maintenance').set_value(False)
            site.get_attribute('done').set_value(False)
            site.get_attribute('name').set_value('__DEFAULT__')

        site.get_attribute('domain').set_value('groupe-bpi.com')
        site.get_attribute('template').set_value('symfony')
        i += 1

    i = 0
    databases = config.get_attribute('databases')

    for platform in databases.get_attribute_names():
        database = databases.get_attribute(platform)

        if i % 2 == 0:
            database.get_attribute('enabled').set_value(True)
        else:
            database.get_attribute('enabled').set_value(False)

        database.get_attribute('name').set_value('%s_name' % platform)
        database.get_attribute('username').set_value('%s_username' % platform)
        database.get_attribute('password').set_value('%s_password' % platform)
        i += 1

    return config


class ConfigurationManager(object):
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
    def get_database_types():
        """
        Returns the hash of available databases technologies supported

        The hash key is the type mnemonique, and the value is the label to be 
        diaplayed.
        """
        return {
            'mysql': 'MySQL',
            'pgsql': 'PostgresQL'
            }

    @staticmethod
    def get_repository_types():
        """
        Returns the hash of available RCS repositories technologies supported

        The hash key is the type mnemonique, and the value is the label to be 
        diaplayed.
        """
        return {
            'svn': 'SVN',
            'git': 'GIT',
            'cvs': 'CVS'
            }

    @staticmethod
    def get_site_platforms():
        """
        Returns a sorted list of available site platfoms.

        The sorted list is mainly used to order components in applicaiton views
        """
        return [ 'prod', 'test', 'dev' ]

    @staticmethod
    def get_database_platforms():
        """
        Returns a sorted list of available database platfoms.

        The sorted list is mainly used to order components in applicaiton views
        """
        return [ 'prod', 'test', 'dev' ]

    @staticmethod
    def get_site_templates():
        """
        Returns the hash of available site templates supported

        The hash key is the template mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            'standard': 'Standard',
            'symfony': 'Symfony',
            'zend': 'Zend'
            }

    @staticmethod
    def get_site_domains():
        """
        Returns the hash of available site domains supported

        The hash key is the domain mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            'bpinet.com': 'bpinet.com',
            'groupe-bpi.com': 'groupe-bpi.com',
            'bpi-group.com': 'bpi-group.com'
            }

    @staticmethod
    def get_blank_configuration():
        """
        Returns a new blank configuration item.
        """
        return AttributeSet(attributes=get_default_config_data())

    @staticmethod
    def get_test_configuration(config_id):
        """
        Returns a new blank configuration item.
        """
        return get_test_configuration(config_id)

    @staticmethod
    def get_configuration_by_id(identifier):
        """
        Loads a configuration item based on its id.
        """
        context = get_application_context()

        if context == 'normal':
            return ConfigurationManager.get_test_configuration_by_id(identifier)
        elif context == 'test':
            return ConfigurationManager.get_real_configuration_by_id(identifier)
        else:
            return None

    @staticmethod
    def get_test_configuration_by_id(identifier):
        """
        If test context is enabled, returns a test configuration set.
        """
        return get_test_configuration(identifier)

    @staticmethod
    def get_real_configuration_by_id(identifier):
        """
        If test context is enabled, returns the real configuration set.
        """
        return get_test_configuration(identifier)

    @staticmethod
    def get_configuration_all():
        """
        Loads all configureation items contained in the configuration
        repository
        """
        context = get_application_context()

        if context == 'normal':
            return ConfigurationManager.get_test_configuration_all()
        elif context == 'test':
            return ConfigurationManager.get_real_configuration_all()
        else:
            return None

    @staticmethod
    def get_test_configuration_all():
        """
        Returns a list of test configuration set
        """
        configurations = []

        for identifier in range(10):
            configurations.append(get_test_configuration(identifier))

        return configurations

    @staticmethod
    def get_real_configuration_all():
        """
        Returns the list of all configuration set contained in the
        configuration repository
        """
        configurations = []

        for identifier in range(10):
            configurations.append(get_test_configuration(identifier))

        return configurations


if __name__ == "__main__":
    import doctest
    doctest.testmod()
