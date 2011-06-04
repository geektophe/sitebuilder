#!/usr/bin/env python

"""
Configuration related classes
"""

from copy import deepcopy


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
    def getDatabaseTypes():
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
    def getRepoTypes():
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
    def getSiteTemplates():
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
    def getSiteDomains():
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
    def getBlankConfigurationItem():
        """
        Returns a new blank configuration item.
        """
        return ConfigurationItem()


    @staticmethod
    def getConfigurationItemById(id):
        """
        Loads a configuration item based on its id.
        """
        config = ConfigurationItem()
        config.load(ConfigurationManager._getTestConfigurationItem())
        return config



    @staticmethod
    def _getTestConfigurationItem(id):
        """
        Generates a sample test configuration dictonnary which attribues are
        filled based on the id number.
        """
        return {
            # General attributes
            'id' : id,
            'reference' : 'reference%s' % id,
            'description' : 'description%s' % id,
            # Repository related attriutes
            'repository' : {
                'enabled' : True,
                'type' : 'svn',
                'name' : 'svn%s' % id,
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
                    'name' : 'test%s' % id
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
                    'name' : 'prod_name%s' % id,
                    'username' : 'prod_username%s' % id,
                    'password' : 'prod_password%s' % id
                    },
                'test' : {
                    'enabled' : True,
                    'done' : True,
                    'type' : 'pgsql',
                    'name' : 'test_name%s' % id,
                    'username' : 'test_username%s' % id,
                    'password' : 'test_password%s' % id
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
        self._config = self._getDefaultConfig()


    def _getDefaultConfig(self):
        """
        Generates the default configuration used to initialize internal
        configuration structure
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


    def getId(self):
        """
        Returns the configuration identifier (generally the database primary
        key)

        >>> config = ConfigurationItem()
        >>> print config.getId()
        None
        """
        return self._config['id']


    def setId(self, value):
        """
        Sets the configuration identifier (generally the database primary
        key)

        >>> config = ConfigurationItem()
        >>> config.setId(1)
        >>> config.getId()
        1
        """
        self._config['id'] = value


    def getReference(self):
        """
        Returns the configuration friendly name

        >>> config = ConfigurationItem()
        >>> config.getReference()
        ''
        """
        return self._config['reference']


    def setReference(self, value):
        """
        Sets the configuration friendly name

        >>> config = ConfigurationItem()
        >>> config.setReference('reference')
        >>> config.getReference()
        'reference'
        """
        self._config['reference'] = value


    def getDescription(self):
        """
        Returns the configuration longer description

        >>> config = ConfigurationItem()
        >>> config.getDescription()
        ''
        """
        return self._config['description']


    def setDescription(self, value):
        """
        Sets the configuration longer description

        >>> config = ConfigurationItem()
        >>> config.setDescription('description')
        >>> config.getDescription()
        'description'
        """
        self._config['description'] = value


    def getRepositoryAttributeNames(self):
        """
        Returns available repository attributes

        >>> config = ConfigurationItem()
        >>> config.getRepositoryAttributeNames()
        ['type', 'enabled', 'name', 'done']
        """
        return self._config['repository'].keys()


    def getRepositoryAttribute(self, attribute):
        """
        Returns attribute's value for repository configuration

        Default value of enabled flag is False

        >>> config = ConfigurationItem()
        >>> config.getRepositoryAttribute('enabled')
        False

        Asking an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.getRepositoryAttribute('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown repository configuration attribute: fake
        """
        if not self._config['repository'].has_key(attribute):
            raise AttributeError(
                'Unknown repository configuration attribute: %s' % attribute)

        return self._config['repository'][attribute]


    def setRepositoryAttribute(self, attribute, value):
        """
        Sets attribute's value for repository configuration

        >>> config = ConfigurationItem()
        >>> config.setRepositoryAttribute('enabled', True)
        >>> config.getRepositoryAttribute('enabled')
        True

        Setting an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.setRepositoryAttribute('fake', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown repository configuration attribute: fake
        """
        if not self._config['repository'].has_key(attribute):
            raise AttributeError(
                'Unknown repository configuration attribute: %s' % attribute)

        self._config['repository'][attribute] = value


    def _getPlatformsFor(self, section):
        """
        Returns available platforms for a given section (sites, databases, ...)
        """
        if not self._config.has_key(section):
            raise AttributeError('Unknown config setion: %s' % section)

        return self._config[section].keys()


    def _getAttributeNamesFor(self, section, platform):
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


    def _getAttributeFor(self, section, platform, attribute):
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


    def _setAttributeFor(self, section, platform, attribute, value):
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


    def getSitesPlatforms(self):
        """
        Returns available sites platforms

        >>> config = ConfigurationItem()
        >>> config.getSitesPlatforms()
        ['test', 'prod', 'dev']
        """
        return self._getPlatformsFor('sites')


    def getSiteAttributeNames(self, platform):
        """
        Returns available site platform attributes

        All platforms do not have the same attributes available

        >>> config = ConfigurationItem()
        >>> config.getSiteAttributeNames('prod')
        ['domain', 'maintenance', 'enabled', 'proxied', 'done', 'template', 'name']
        >>> config.getSiteAttributeNames('dev')
        ['domain', 'maintenance', 'enabled', 'done', 'template', 'name']

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.getSiteAttributeNames('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites platform: fake
        """
        return self._getAttributeNamesFor('sites', platform)


    def getSiteAttribute(self, platform, attribute):
        """
        Returns attribute's value for a specific platform from sites
        configuration.

        >>> config = ConfigurationItem()
        >>> config.getSiteAttribute('prod', 'enabled')
        False

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.getSiteAttribute('fake', 'enabled')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites platform: fake

        Asking an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.getSiteAttribute('prod', 'fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites attribute: fake
        """
        return self._getAttributeFor('sites', platform, attribute)

    def setSiteAttribute(self, platform, attribute, value):
        """
        Sets attribute's value for a specific platform from sites
        configuration.

        >>> config = ConfigurationItem()
        >>> config.setSiteAttribute('prod', 'enabled', True)
        >>> config.getSiteAttribute('prod', 'enabled')
        True

        Using an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.setSiteAttribute('fake', 'enabled', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites platform: fake

        Setting an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.setSiteAttribute('prod', 'fake', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown sites attribute: fake
        """
        self._setAttributeFor('sites', platform, attribute, value)


    def getDatabasesPlatforms(self):
        """
        Returns available databases platforms

        >>> config = ConfigurationItem()
        >>> config.getDatabasesPlatforms()
        ['test', 'prod', 'dev']
        """
        return self._getPlatformsFor('databases')


    def getDatabaseAttributeNames(self, platform):
        """
        Returns available database platform attributes

        >>> config = ConfigurationItem()
        >>> config.getDatabaseAttributeNames('prod')
        ['username', 'name', 'enabled', 'done', 'password', 'type']

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.getDatabaseAttributeNames('fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases platform: fake
        """
        return self._getAttributeNamesFor('databases', platform)


    def getDatabaseAttribute(self, platform, attribute):
        """
        Returns attribute's value for a specific platform from databases
        configuration

        >>> config = ConfigurationItem()
        >>> config.getDatabaseAttribute('prod', 'enabled')
        False

        Asking an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.getDatabaseAttribute('fake', 'enabled')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases platform: fake

        Asking an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.getDatabaseAttribute('prod', 'fake')
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases attribute: fake
        """
        return self._getAttributeFor('databases', platform, attribute)


    def setDatabaseAttribute(self, platform, attribute, value):
        """
        Sets attribute's value for a specific platform from databases
        configuration

        >>> config = ConfigurationItem()
        >>> config.setDatabaseAttribute('prod', 'enabled', True)
        >>> config.getDatabaseAttribute('prod', 'enabled')
        True

        Using an unknown platform should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.setDatabaseAttribute('fake', 'enabled', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases platform: fake

        Setting an unknown attribute should raise an AttributeError

        >>> config = ConfigurationItem()
        >>> config.setDatabaseAttribute('prod', 'fake', True)
        Traceback (most recent call last):
            ...
        AttributeError: Unknown databases attribute: fake
        """
        self._setAttributeFor('databases', platform, attribute, value)


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
        >>> config.getId()
        1
        >>> config.getReference()
        'ref1'
        >>> config.getDescription()
        'desc1'
        >>> config.getRepositoryAttribute('enabled')
        True
        >>> config.getRepositoryAttribute('name')
        'svn1'
        >>> config.getSiteAttribute('prod', 'enabled')
        True
        >>> config.getSiteAttribute('prod', 'name')
        'prod1'
        >>> config.getDatabaseAttribute('prod', 'enabled')
        True
        >>> config.getDatabaseAttribute('prod', 'name')
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
        >>> print config.getId()
        None
        """
        localConfig = deepcopy(self._config)
        self._loadRecursive(localConfig, config)
        self._config = localConfig


    def _loadRecursive(self, base, config):
        """
        Recursively loads a configuration dictionnary into the internal,
        configuration. An unknown attribute name should raise an
        AttributeError.
        """
        for (name, value) in config.iteritems():

            if not base.has_key(name):
                raise AttributeError("Unknown attribute: %s" % name)

            if isinstance(value, dict):
                self._loadRecursive(base[name], config[name])
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
