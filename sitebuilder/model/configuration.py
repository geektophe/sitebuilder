#!/usr/bin/env python

"""
Configuration related classes
"""

from copy import deepcopy
import re


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


class Attribute(object):
    """
    A configuration attribute item that is part of a configuration tree.

    Each configuration attribute is identified by its name, and can be get or
    set its value.

    It also presents a validate method that checks that the current value is
    valid. The value validity checking is performed by default by checking if
    is matches a regular expression that may be changed. Subclasses may
    implement their own validity checking method. The load method has to be
    overloeded also to take in consideration this change.

    As the attribute is part of a tree, it is possible to check whether the
    it has childs using has_children, and childre can be fetched using
    get_children method.

    A load method is also available to build a configuration tree composed of
    attribute objects from an input dictionnary. The corresponding dump method
    is also available to dump the current configuartion as a dictionnary.
    """

    def __init__(self, name, value=None, vregex=None):
        """
        Object initialization. The only mandatory argument is the attribute
        name, that cannot be changed later.
        """
        self._name = name
        self._value = value
        self._vregex = vregex
        self._modified = False

        if vregex is not None:
            self._validator = re.compile(vregex)
        else:
            self._validator = None

    def get_name(self):
        """
        Returns attribute name

        >>> attr = Attribute(name='somename')
        >>> attr.get_name()
        'somename'
        """
        return self._name

    def get_vregex(self):
        """
        Returns attribute validation regex

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.get_vregex()
        '^[\\\\d]+$'
        """
        return self._vregex

    def check(self, value):
        """
        Checks whether an input value is valid

        If a regex is passed at instanciation, it should be used to check
        against data valididty

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.check(5)
        True
        >>> attr.check('somestring')
        False

        If none is defined, a value should always ve valid

        >>> attr = Attribute(name='somename')
        >>> attr.check(5)
        True
        >>> attr.check('somestring')
        True
        """
        if self._validator is None:
            return True
        else:
            return (self._validator.match(str(value)) is not None)

    def get_value(self):
        """
        Returns current value

        >>> attr = Attribute(name='somename', value='somevalue')
        >>> attr.get_value()
        'somevalue'
        """
        return self._value

    def set_value(self, value, check=True):
        """
        Sets current value.

        >>> attr = Attribute(name='somename')
        >>> attr.set_value('somevalue')
        >>> attr.get_value()
        'somevalue'

        If a validatoin regex is passed at instanciation, it should be used to
        check against data validity.

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value(5)
        >>> attr.get_value()
        5

        If an invalid data is passed, an AttributeError should be raised.

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value('somevalue')
        Traceback (most recent call last):
            ...
        AttributeError: Invalid input data

        Finally, if the user interface has previously checked data with the
        check method, in order to avoid double check, it is possible to disable
        data check. This way, any data should be set.

        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value(5, False)
        >>> attr.get_value()
        5
        >>> attr.set_value('somevalue', False)
        >>> attr.get_value()
        'somevalue'

        A value set should enable the modified flag
        >>> attr = Attribute(name='somename', vregex=r'^[\d]+$')
        >>> attr.set_value(5, False)
        >>> attr.is_modified()
        True
        """
        if check is True and self.check(value) is False:
            # TODO: be more descriptive
            raise AttributeError('Invalid input data')
        self._value = value
        self._modified = True

    def is_modified(self):
        """
        Returns the modified flag
        """
        return self._modified

    def clear_modified(self):
        """
        Resets the modified flag
        """
        self._modified = False

    def __str__(self):
        """
        Returns object string representation.
        """
        return '<Attribute object {name: %s, vregex: %s, value: %s}>' % \
            (self._name, self._vregex, self._value)


class AttributeSet(object):
    """
    A class that represents a set of attributes.

    Each attrbiute can be fetched using its name (get_attribute), or through
    an iterator (for statement).

    A load method allows to load a set of predefined attributes from
    dictionary (see load method docstring for details)

    """

    def __init__(self, name, attributes=None):
        self._name = name
        self._attributes = {}

        if  attributes is not None:
            self.load(attributes)

    def get_name(self):
        """
        Returns attribute set name

        >>> aset = AttributeSet('aset')
        >>> aset.get_name()
        'aset'
        """
        return self._name

    def load(self, attributes):
        """
        = Attribute set loading from dictionnary

        The load method allows to load a set of predefined attributes from
        dictionary using the following formalism:

        - Each key represents an attribute name.
        - If dictionary's associated value is a tupple, then a new Attribute
        object should be instanciated (see Attribute loading from tupple
        section below for details on Attribute formalism)
        - If the associated value is another dictionnary, then it should be
        loaded as sub AttributeSet.

        = Attrribute loading from tuppple

        When a tupple is detected in a dictionary value, it is loaded as an
        Attribute object. The tupple must stick the following formalism :

        (value, vregex, verrdescr)

        Where 'name' is the attribute name, 'vregex' is the attrbibute regex
        used to check attribute value vaidity while using set_attrbiute methid
        (should be None if you don't want to apply value cehcking), and 'value'
        is the initial attrbiute value (should be None if you don't knwo it).

        >>> attributes = {}
        >>> attributes['somename'] = ('somevalue', None, None)
        >>> attributes['sub'] = {}
        >>> attributes['sub']['someothername'] = ('someothervalue', '^[\w]+$',
        ...                                       'Value should be a string')
        >>> aset = AttributeSet('aset')
        >>> aset.load(attributes)
        >>> attr = aset.get_attribute('somename')
        >>> isinstance(attr, Attribute)
        True
        >>> attr.get_name()
        'somename'
        >>> attr.get_value()
        'somevalue'
        >>> sub = aset.get_attribute('sub')
        >>> isinstance(sub, AttributeSet)
        True
        >>> subattr = sub.get_attribute('someothername')
        >>> subattr.get_name()
        'someothername'
        >>> subattr.get_value()
        'someothervalue'

        The load operation should also be atomic. If an attribute loading
        fails, the whole loading should be rollbacked.
        """
        new_attributes = {}

        for key, value in attributes.iteritems():
            if isinstance(value, tuple):
                new_attributes[key] = Attribute(key, value[0], value[1])
            elif isinstance(value, dict):
                new_attributes[key] = AttributeSet(key)
                new_attributes[key].load(value)
            else:
                raise AttributeError('Invalid data format for key %s' % key)

            self._attributes = new_attributes

    def get_attribute(self, name):
        """
        Returns attribute named 'name'

        >>> attributes = {'somename': ('somevalue', None, None)}
        >>> aset = AttributeSet('aset', attributes)
        >>> attr = aset.get_attribute('somename')
        >>> isinstance(attr, Attribute)
        True
        >>> attr.get_value()
        'somevalue'

        If attribute does not exist, it should raise ne exception.

        >>> aset = AttributeSet('aset')
        >>> attr = aset.get_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'
        """
        if not self._attributes.has_key(name):
            raise AttributeError("No attribute named '%s'" % name)

        return self._attributes[name]

    def del_attribute(self, name):
        """
        Deletes attribute named 'name'

        >>> attributes = {'somename': ('somevalue', None, None)}
        >>> aset = AttributeSet('aset', attributes)
        >>> attr = aset.del_attribute('somename')
        >>> attr = aset.get_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'

        If attribute does not exist, it should raise ne exception.

        >>> aset = AttributeSet('aset')
        >>> attr = aset.del_attribute('somename')
        Traceback (most recent call last):
            ...
        AttributeError: No attribute named 'somename'
        """
        if not self._attributes.has_key(name):
            raise AttributeError("No attribute named '%s'" % name)

        del self._attributes[name]

    def get_attribute_names(self):
        """
        Returns the list of contained attributes

        >>> attributes = {}
        >>> attributes['somename'] = ('somevalue', None, None)
        >>> attributes['someothername'] = ('someothervalue', None, None)
        >>> aset = AttributeSet('aset', attributes)
        >>> aset.get_attribute_names()
        ['somename', 'someothername']
        """
        return self._attributes.keys()

    def add_attribute(self, attribute):
        """
        Adds an Attribute anr an AttributeSet.

        The key under which the attribute is stored is the same as the
        attribute name

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = AttributeSet('someothername')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> attr3 = aset.get_attribute('somename')
        >>> isinstance(attr3, Attribute)
        True
        >>> attr3.get_value()
        'somevalue'
        >>> attr3 = aset.get_attribute('someothername')
        >>> isinstance(attr3, AttributeSet)
        True

        Only Attribute and AttributteSet types are allowed.

        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute('string')
        Traceback (most recent call last):
            ...
        AttributeError: Invalid attribute type. Only Attribute and AttributeSet allowed.

        Adding attributes whiche name are the same is forbidden.

        >>> aset = AttributeSet('aset')
        >>> attr1 = Attribute('somename')
        >>> attr2 = Attribute('somename')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        Traceback (most recent call last):
            ...
        AttributeError: Attribute name 'somename' already exists.
        """
        if not isinstance(attribute, Attribute) and \
                not isinstance(attribute, AttributeSet):

            raise AttributeError(
                'Invalid attribute type. ' +
                'Only Attribute and AttributeSet allowed.')

        if self._attributes.has_key(attribute.get_name()):
            raise AttributeError("Attribute name '%s' already exists." %
                                attribute.get_name())

        self._attributes[attribute.get_name()] = attribute

    def iteritems(self):
        """
        Returns an iterator on attributes

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> [ (key, value.get_value()) for key, value in aset.iteritems() ]
        [('somename', 'somevalue'), ('someothername', 'someothervalue')]
        """
        return self._attributes.iteritems()

    def items(self):
        """
        Returns attributes keys and values

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> [ (key, value.get_value()) for key, value in aset.items() ]
        [('somename', 'somevalue'), ('someothername', 'someothervalue')]
        """
        return self._attributes.iteritems()

    def keys(self):
        """
        Returns attributes keys

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> aset.keys()
        ['somename', 'someothername']
        """
        return self._attributes.keys()

    def values(self):
        """
        Returns attributes keys

        >>> attr1 = Attribute('somename', 'somevalue')
        >>> attr2 = Attribute('someothername', 'someothervalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr1)
        >>> aset.add_attribute(attr2)
        >>> [ value.get_value() for  value in aset.values() ]
        ['somevalue', 'someothervalue']
        """
        return self._attributes.values()

    def has_key(self, key):
        """
        Checks whether an attribute is registered as key

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> aset.has_key('somename')
        True
        >>> aset.has_key('someothername')
        False
        """
        return self._attributes.has_key(key)

    def clear(self):
        """
        Clears internal dictionnary

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> aset.has_key('somename')
        True
        >>> aset.clear()
        >>> aset.has_key('somename')
        False
        """
        return self._attributes.clear()

    def get(self, key, default=None):
        """
        Gets value from dictionnary. If key does not exist, returnd default.

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> attr2 = aset.get('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> attr.get_value()
        'somevalue'
        >>> attr3 = aset.get('someothername')
        >>> attr3 is None
        True
        """
        return self._attributes.get(key, default)

    def pop(self, key, default=None):
        """
        Pops an element from the internal dictionnary

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> attr2 = aset.pop('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> attr2.get_value()
        'somevalue'
        >>> aset.has_key('somename')
        False
        >>> attr3 = aset.pop('somename')
        >>> attr3 is None
        True
        """
        return self._attributes.pop(key, default)

    def __getitem__(self, name):
        """
        Dictionnary like magic method

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset.add_attribute(attr)
        >>> attr2 = aset['somename']
        >>> isinstance(attr2, Attribute)
        True
        >>> attr2.get_name()
        'somename'
        >>> attr2.get_value()
        'somevalue'
        """
        return self.get_attribute(name)

    def __setitem__(self, name, attribute):
        """
        Dictionnary like magic method.

        Caution, the key used is the real object name, not the name parameter.

        >>> attr = Attribute('somename', 'somevalue')
        >>> aset = AttributeSet('aset')
        >>> aset['somename'] = attr
        >>> attr2 = aset.get_attribute('somename')
        >>> isinstance(attr2, Attribute)
        True
        >>> attr2.get_name()
        'somename'
        >>> attr2.get_value()
        'somevalue'
        """
        self.add_attribute(attribute)

    def __str__(self):
        """
        Returns internal attributes string representation.
        """
        return str(self._attributes)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
