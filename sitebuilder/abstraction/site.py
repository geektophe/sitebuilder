#!/usr/bin/env python

"""
Configuration related classes
"""

from sitebuilder.utils.parameters import get_application_context
from sitebuilder.abstraction.attribute import AttributeSet


def get_default_config_data():
    """
    Generates the default configuration used to initialize internal
    configuration structures
    """
    return {
        # General attributes
        'general' : {
            'id' : (None, int, 'Id should be a number'),
            'platform' : (SiteConfigurationManager.get_default_platform(),
                          SiteConfigurationManager.get_platforms().keys(),
                          'Unknown platform'),
            'domain' : (SiteConfigurationManager.get_default_domain(),
                        SiteConfigurationManager.get_domains().keys(),
                        'Unknown domain'),
            'name' : ('', '^[\d\w_-]*$', 'Name should be an alphanumeric string'),
            'description' : ('', None),
            'done' : (False, bool),
            },
        # Repository related attriutes
        'repository' : {
            'enabled' : (False, bool),
            'type' : (SiteConfigurationManager.get_default_repository_type(),
                      SiteConfigurationManager.get_repository_types().keys(),
                      'Unsupported RCS type'),
            'name' : ('', '^[\d\w_-]*$', 'Name should be an alphanumeric string or _, without spaces'),
            'done' : (False, bool)
            },
        # Sites related attributes (for each available platform)
        'website' : {
            'enabled' : (False, bool),
            'access' : (SiteConfigurationManager.get_default_access(),
                        SiteConfigurationManager.get_site_accesses().keys(),
                        'Unsupported access'),
            'maintenance' : (False, bool),
            'template' : ('standard',
                          SiteConfigurationManager.get_site_templates().keys(),
                          'Unsupported site template'),
            'done' : (False, bool)
            },
        # Databases related attributes (for each available platform)
        'database' : {
            'enabled' : (False, bool),
            'type' : (SiteConfigurationManager.get_default_database_type(),
                      SiteConfigurationManager.get_database_types().keys(),
                      'Unsupported database type'),
            'name' : ('', '^[a-z0-9_]+$', 'Name should be a simple alphanumeric string without spaces'),
            'username' : ('', '^[a-z0-9_]+$', 'Username should be a simple alphanumeric string without spaces'),
            'password' : ('', None),
            'done' : (False, bool)
            },
        }


def get_test_configuration(config_id):
    """
    Generates the default configuration used to initialize internal
    configuration structures
    """
    config = SiteConfigurationManager.get_blank_configuration()

    general = config.get_attribute('general')
    general.get_attribute('id').set_value(config_id)
    general.get_attribute('name').set_value('name%d' % config_id)
    general.get_attribute('description').set_value('desc%d' % config_id)

    repository = config.get_attribute('repository')
    repository.get_attribute('enabled').set_value(True)
    repository.get_attribute('done').set_value(True)

    website = config.get_attribute('website')
    website.get_attribute('enabled').set_value(True)
    website.get_attribute('maintenance').set_value(True)
    website.get_attribute('done').set_value(True)

    database = config.get_attribute('database')
    database.get_attribute('enabled').set_value(True)
    database.get_attribute('name').set_value('%s_name' % config_id)
    database.get_attribute('username').set_value('%s_username' % config_id)
    database.get_attribute('password').set_value('%s_password' % config_id)
    database.get_attribute('done').set_value(True)

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
    def get_default_database_type():
        """
        Returns the default databases technology.

        Note that only the mnemonique is returned, not the associated label
        """
        return 'mysql'

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
    def get_default_repository_type():
        """
        Returns the hash of available RCS repositories technologies supported

        Note that only the mnemonique is returned, not the associated label
        """
        return 'svn'

    @staticmethod
    def get_platforms():
        """
        Returns a sorted list of available site platfoms.

        The sorted list is mainly used to order components in applicaiton views
        """
        return { 'prod': 'Prod', 'test': 'Test', 'dev': 'Dev' }

    @staticmethod
    def get_default_platform():
        """
        Returns the default platform name.

        Note that only the mnemonique is returned, not the associated label
        """
        return 'prod'

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
    def get_default_site_template():
        """
        Returns the default site template

        Note that only the mnemonique is returned, not the associated label
        """
        return 'standard'

    @staticmethod
    def get_site_accesses():
        """
        Returns the hash of available web sutes access types supported

        The hash key is the template mnemonique, and the value is the label to
        be diaplayed.
        """
        return {
            'internal': 'Internal only',
            'external': 'Internal / External',
            'custom': 'Custom'
            }

    @staticmethod
    def get_default_access():
        """
        Returns the default site access type

        Note that only the mnemonique is returned, not the associated label
        """
        return 'internal'

    @staticmethod
    def get_domains():
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
    def get_default_domain():
        """
        Returns the available domain name

        Note that only the mnemonique is returned, not the associated label
        """
        return 'bpinet.com'

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
            return SiteConfigurationManager.get_test_configuration_by_id(
                    identifier)
        elif context == 'test':
            return SiteConfigurationManager.get_real_configuration_by_id(
                    identifier)
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
