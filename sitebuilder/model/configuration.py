#!/usr/bin/env python

"""
Configuration related classes
"""

from copy import deepcopy


###############################################################################

def get_default_config():
    """
    Generates the default configuration used to initialize internal
    configuration structures
    """
    return {
        # General attributes
        'id' : None,
        'reference' : '',
        'description' : '',
        # Repository related attriutes
        'repository' : {
            'enabled' : False,
            'type' : 'svn',
            'name' : '',
            'done' : False
            },
        # Sites related attributes (for each available platform)
        'sites' : {
            'prod' : {
                'enabled' : False,
                'proxied' : False,
                'maintenance' : False,
                'done' : False,
                'template' : 'standard',
                'domain' : 'bpinet.com',
                'name' : '__DEFAULT__'
                },
            'test' : {
                'enabled' : False,
                'proxied' : False,
                'maintenance' : False,
                'done' : False,
                'template' : 'standard',
                'domain' : 'bpinet.com',
                'name' : '__DEFAULT__'
                },
            'dev' : {
                'enabled' : False,
                'maintenance' : False,
                'done' : False,
                'template' : 'standard',
                'domain' : 'bpinet.com',
                'name' : '__DEFAULT__'
                },
            },
        # Databases related attributes (for each available platform)
        'databases' : {
            'prod' : {
                'enabled' : False,
                'done' : False,
                'type' : 'mysql',
                'name' : '',
                'username' : '',
                'password' : ''
                },
            'test' : {
                'enabled' : False,
                'done' : False,
                'type' : 'mysql',
                'name' : '',
                'username' : '',
                'password' : ''
                },
            'dev' : {
                'enabled' : False,
                'done' : False,
                'type' : 'mysql',
                'name' : '',
                'username' : '',
                'password' : ''
                },
            }
        }


###############################################################################

def get_test_configuration_item(identifier):
    """
    Generates a sample test configuration dictonnary which attribues are
    filled based on the id number.
    """
    return {
        # General attributes
        'id' : identifier,
        'reference' : 'reference%s' % identifier,
        'description' : 'description%s' % identifier,
        # Repository related attriutes
        'repository' : {
            'enabled' : True,
            'type' : 'svn',
            'name' : 'svn%s' % identifier,
            'done' : False
            },
        # Sites related attributes (for each available platform)
        'sites' : {
            'prod' : {
                'enabled' : True,
                'proxied' : True,
                'maintenance' : False,
                'done' : False,
                'template' : 'standard',
                'domain' : 'bpi-group.com',
                'name' : '__DEFAULT__'
                },
            'test' : {
                'enabled' : True,
                'proxied' : True,
                'maintenance' : True,
                'done' : True,
                'template' : 'symfony',
                'domain' : 'bpi-group.com',
                'name' : 'test%s' % identifier
                },
            'dev' : {
                'enabled' : False,
                'maintenance' : False,
                'done' : False,
                'template' : 'standard',
                'domain' : 'bpinet.com',
                'name' : '__DEFAULT__'
                },
            },
        # Databases related attributes (for each available platform)
        'databases' : {
            'prod' : {
                'enabled' : True,
                'done' : False,
                'type' : 'pgsql',
                'name' : 'prod_name%s' % identifier,
                'username' : 'prod_username%s' % identifier,
                'password' : 'prod_password%s' % identifier
                },
            'test' : {
                'enabled' : True,
                'done' : True,
                'type' : 'pgsql',
                'name' : 'test_name%s' % identifier,
                'username' : 'test_username%s' % identifier,
                'password' : 'test_password%s' % identifier
                },
            'dev' : {
                'enabled' : False,
                'done' : False,
                'type' : 'mysql',
                'name' : '',
                'username' : '',
                'password' : ''
                },
            }
        }


###############################################################################

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
    def get_blank_configuration_item():
        """
        Returns a new blank configuration item.
        """
        return ConfigurationItem()


    @staticmethod
    def get_configuration_item_by_id(identifier):
        """
        Loads a configuration item based on its id.
        """
        config = ConfigurationItem()
        config.load(get_test_configuration_item(identifier))
        return config


###############################################################################

class ConfigurationItem(object):
    """
    Configuration item base class (to be subclassed) that implements
    configurations items default behaviours.

    A configuration item represents the system requirements for a given
    application (such as web sites, databases to be created, proxy
    configuration, and so on. But it also represents the current state of the
    creation process through the 'done' flag associated to certain parts of the
    configuration.

    It also supports loading and dumping internal configuration structures.

    Finally, it defines the default values of each configuration section.
    """


    def __init__(self):
        """
        Initializes the internal configuration hash
        """
        self._config = get_default_config()

    def get_id(self):
        """
        Returns the configuration identifier (generally the database primary
        key)

        >>> config = ConfigurationItem()
        >>> print config.get_id()
        None
        """
        return self._config['id']

    def set_id(self, value):
        """
        Sets the configuration identifier (generally the database primary
        key)

        >>> config = ConfigurationItem()
        >>> config.set_id(1)
        >>> config.get_id()
        1
        """
        self._config['id'] = value

    def get_reference(self):
        """
        Returns the configuration friendly name

        >>> config = ConfigurationItem()
        >>> config.get_reference()
        ''
        """
        return self._config['reference']

    def set_reference(self, value):
        """
        Sets the configuration friendly name

        >>> config = ConfigurationItem()
        >>> config.set_reference('reference')
        >>> config.get_reference()
        'reference'
        """
        self._config['reference'] = value

    def get_description(self):
        """
        Returns the configuration longer description

        >>> config = ConfigurationItem()
        >>> config.get_description()
        ''
        """
        return self._config['description']

    def set_description(self, value):
        """
        Sets the configuration longer description

        >>> config = ConfigurationItem()
        >>> config.set_description('description')
        >>> config.get_description()
        'description'
        """
        self._config['description'] = value

    def get_repository_attribute_names(self):
        """
        Returns available repository attributes

        >>> config = ConfigurationItem()
        >>> config.get_repository_attribute_names()
        ['type', 'enabled', 'name', 'done']
        """
        return self._config['repository'].keys()

    def get_repository_attribute(self, attribute):
        """
        Returns attribute's value for repository configuration

        Default value of enabled flag is False

        >>> config = ConfigurationItem()
        >>> config.get_repository_attribute('enabled')
        False

        Asking an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.get_repository_attribute('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown repository configuration attribute: fake
        """
        if not self._config['repository'].has_key(attribute):
            raise AttributeError(
                'Unknown repository configuration attribute: %s' % attribute)

        return self._config['repository'][attribute]

    def set_repository_attribute(self, attribute, value):
        """
        Sets attribute's value for repository configuration

        >>> config = ConfigurationItem()
        >>> config.set_repository_attribute('enabled', True)
        >>> config.get_repository_attribute('enabled')
        True

        Setting an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.set_repository_attribute('fake', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown repository configuration attribute: fake
        """
        if not self._config['repository'].has_key(attribute):
            raise AttributeError(
                'Unknown repository configuration attribute: %s' % attribute)

        self._config['repository'][attribute] = value

    def _get_platforms_for(self, section):
        """
        Returns available platforms for a given section (sites, databases, ...)
        """
        if not self._config.has_key(section):
            raise AttributeError('Unknown config setion: %s' % section)

        return self._config[section].keys()

    def _get_attribute_names_for(self, section, platform):
        """
        Returns available platform attributes for a given section (sites,
        databases, ...)
        """
        if not self._config.has_key(section):
            raise AttributeError('Unknown config setion: %s' % section)

        if not self._config[section].has_key(platform):
            raise AttributeError('Unknown %s platform: %s' %
                                 (section, platform))

        return self._config[section][platform].keys()

    def _get_attribute_for(self, section, platform, attribute):
        """
        Returns attribute's value for a specific platform for a given section
        (sites, databases, ...)
        """
        if not self._config.has_key(section):
            raise AttributeError('Unknown config setion: %s' % section)

        if not self._config[section].has_key(platform):
            raise AttributeError('Unknown %s platform: %s' %
                                 (section, platform))

        if not self._config[section][platform].has_key(attribute):
            raise AttributeError('Unknown %s attribute: %s' %
                                 (section, attribute))

        return self._config[section][platform][attribute]

    def _set_attribute_for(self, section, platform, attribute, value):
        """
        Sets attribute's value for a specific platform for a given section
        (sites, databases, ...)
        """
        if not self._config.has_key(section):
            raise AttributeError('Unknown config setion: %s' % section)

        if not self._config[section].has_key(platform):
            raise AttributeError('Unknown %s platform: %s' %
                                 (section, platform))

        if not self._config[section][platform].has_key(attribute):
            raise AttributeError('Unknown %s attribute: %s' %
                                 (section, attribute))

        self._config[section][platform][attribute] = value

    def get_site_platforms(self):
        """
        Returns available sites platforms

        >>> config = ConfigurationItem()
        >>> config.get_site_platforms()
        ['test', 'prod', 'dev']
        """
        return self._get_platforms_for('sites')

    def get_site_attribute_names(self, platform):
        """
        Returns available site platform attributes

        All platforms do not have the same attributes available

        >>> config = ConfigurationItem()
        >>> config.get_site_attribute_names('prod')
        ['domain', 'maintenance', 'enabled', 'proxied', 'done', 'template', 'name']
        >>> config.get_site_attribute_names('dev')
        ['domain', 'maintenance', 'enabled', 'done', 'template', 'name']

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.get_site_attribute_names('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites platform: fake
        """
        return self._get_attribute_names_for('sites', platform)

    def get_site_attribute(self, platform, attribute):
        """
        Returns attribute's value for a specific platform from sites
        configuration.

        >>> config = ConfigurationItem()
        >>> config.get_site_attribute('prod', 'enabled')
        False

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.get_site_attribute('fake', 'enabled')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites platform: fake

        Asking an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.get_site_attribute('prod', 'fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites attribute: fake
        """
        return self._get_attribute_for('sites', platform, attribute)

    def set_site_attribute(self, platform, attribute, value):
        """
        Sets attribute's value for a specific platform from sites
        configuration.

        >>> config = ConfigurationItem()
        >>> config.set_site_attribute('prod', 'enabled', True)
        >>> config.get_site_attribute('prod', 'enabled')
        True

        Using an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.set_site_attribute('fake', 'enabled', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites platform: fake

        Setting an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.set_site_attribute('prod', 'fake', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites attribute: fake
        """
        self._set_attribute_for('sites', platform, attribute, value)

    def get_database_platforms(self):
        """
        Returns available databases platforms

        >>> config = ConfigurationItem()
        >>> config.get_database_platforms()
        ['test', 'prod', 'dev']
        """
        return self._get_platforms_for('databases')

    def get_database_attribute_names(self, platform):
        """
        Returns available database platform attributes

        >>> config = ConfigurationItem()
        >>> config.get_database_attribute_names('prod')
        ['username', 'name', 'enabled', 'done', 'password', 'type']

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.get_database_attribute_names('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases platform: fake
        """
        return self._get_attribute_names_for('databases', platform)

    def get_database_attribute(self, platform, attribute):
        """
        Returns attribute's value for a specific platform from databases
        configuration

        >>> config = ConfigurationItem()
        >>> config.get_database_attribute('prod', 'enabled')
        False

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.get_database_attribute('fake', 'enabled')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases platform: fake

        Asking an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.get_database_attribute('prod', 'fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases attribute: fake
        """
        return self._get_attribute_for('databases', platform, attribute)

    def set_database_attribute(self, platform, attribute, value):
        """
        Sets attribute's value for a specific platform from databases
        configuration

        >>> config = ConfigurationItem()
        >>> config.set_database_attribute('prod', 'enabled', True)
        >>> config.get_database_attribute('prod', 'enabled')
        True

        Using an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.set_database_attribute('fake', 'enabled', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases platform: fake

        Setting an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.set_database_attribute('prod', 'fake', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases attribute: fake
        """
        self._set_attribute_for('databases', platform, attribute, value)

    def load(self, config):
        """
        Loads the content of the config dictionnary passed as parameter into
        the internal configuration.

        A cnfiguration attribute is only loaded if the corresponding option
        already exists into the internal configuration.

        >>> to_load = {}
        >>> to_load['id'] = 1
        >>> to_load['reference'] = 'ref1'
        >>> to_load['description'] = 'desc1'
        >>> to_load['repository'] =  { 'enabled' : True, 'name' : 'svn1' }
        >>> to_load['sites'] =  {'prod' : {'enabled': True, 'name' : 'prod1'}}
        >>> to_load['databases'] =  {'prod' : {'enabled': True, 'name' : 'db1'}}
        >>> config = ConfigurationItem()
        >>> config.load(to_load)
        >>> config.get_id()
        1
        >>> config.get_reference()
        'ref1'
        >>> config.get_description()
        'desc1'
        >>> config.get_repository_attribute('enabled')
        True
        >>> config.get_repository_attribute('name')
        'svn1'
        >>> config.get_site_attribute('prod', 'enabled')
        True
        >>> config.get_site_attribute('prod', 'name')
        'prod1'
        >>> config.get_database_attribute('prod', 'enabled')
        True
        >>> config.get_database_attribute('prod', 'name')
        'db1'

        Trying to load a configuration dictionnary with an unknown attribute should
        raise an AttributeError.

        >>> to_load = { 'fake' : 1 }
        >>> to_load['fake'] = 1
        >>> config = ConfigurationItem()
        >>> config.load(to_load)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown attribute: fake

        >>> to_load = {'databases': {'prod' : {'fake': True}}}
        >>> config = ConfigurationItem()
        >>> config.load(to_load)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown attribute: fake

        The load operation is atomic. If one attribute load fails, none is
        updated.

        >>> to_load = {'id' : 1, 'databases': {'prod' : {'fake': True}}}
        >>> config = ConfigurationItem()
        >>> config.load(to_load)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown attribute: fake
        >>> print config.get_id()
        None
        """
        local_config = deepcopy(self._config)
        self._load_recursive(local_config, config)
        self._config = local_config

    def _load_recursive(self, base, config):
        """
        Recursively loads a configuration dictionnary into the internal,
        configuration. An unknown attribute name should raise an
        AttributeError.
        """
        for (name, value) in config.iteritems():

            if not base.has_key(name):
                raise AttributeError("Unknown attribute: %s" % name)

            if isinstance(value, dict):
                self._load_recursive(base[name], config[name])
            else:
                base[name] = value

    def dump(self):
        """
        Dumps the internal configuration dictionnary. The dumped dictionnary
        is a deep copy of the configuration to prevent modification of the
        internal configuration without using the dedicated methods.

        >>> config = ConfigurationItem()
        >>> dumped = config.dump()
        >>> print dumped['id']
        None
        >>> dumped['reference']
        ''
        >>> dumped['sites']['prod']['enabled']
        False
        """
        return deepcopy(self._config)

    def __str__(self):
        """
        Configuration string representation
        """
        return str(self._config)


###############################################################################

class BlankConfigurationItem(ConfigurationItem):
    """
    Blank configuration item. Mainly used when a new configuration item has to
    be created.

    As a subclass of ConfigurationItem, it sets the
    configuration default values, and ca be used to load a set of existing
    configuration attributes.
    """
    pass


###############################################################################

if __name__ == "__main__":
    import doctest
    doctest.testmod()
