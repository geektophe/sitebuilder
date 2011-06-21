#!/usr/bin/env python

"""
Configuration related classes
"""

from sitebuilder.utils.attribute import Attribute, AttributeSet


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
        return MainConfigurationItem()


    @staticmethod
    def get_configuration_item_by_id(identifier):
        """
        Loads a configuration item based on its id.
        """
        config = MainConfigurationItem()
        config.load(get_test_configuration_item(identifier))
        return config


###############################################################################

class BaseConfigurationItem(object):
    """
    Base class to implement configuration items
    """

    def __init__(self, attrdict=None):
        """
        Initializes the internal configuration object
        """
        if attrdict is None:
            self._config = AttributeSet()
        else:
            self.load(attrdict)

    def get_attribute(self, name):
        """
        Returns Attribute object identified by name. If name does not exist,
        return None.
        """
        if not self._config.has_key(name):
            return None

        attr =  self._config[name]

        if isinstance(attr, Attribute):
            return attr
        else:
            return BaseConfigurationItem(attr)

    def get_attribute_names(self):
        """
        Returns attributes names from internal configuration object
        """
        return self._config.keys()

    def load(self, attrdict):
        """
        Loads the content of the config dictionnary passed as parameter into
        the internal configuration.

        Load mehtod expects attrdict parameter to conform to AtributeSet
        attridict parameter.

        >>> attrdict = {
        ...     'somename' : ('somevalue', r'^\w+$', 'Only letters'),
        ...     'somesubattr': {
        ...         'someothername': ('someothervalue', r'^\w+$', 'Only letters')
        ...         }
        ...     }
        >>> config = BaseConfigurationItem()
        >>> config.load(attrdict)
        >>> config.get_attribute_names()
        ['somesubattr', 'somename']
        >>> attr = config.get_attribute('somename')
        >>> isinstance(attr, Attribute)
        True
        >>> attr.get_value()
        'somevalue'
        >>> subattr = config.get_attribute('somesubattr')
        >>> isinstance(subattr, BaseConfigurationItem)
        True
        >>> subattr.get_attribute_names()
        ['someothername']
        >>> subsubattr = subattr.get_attribute('someothername')
        >>> isinstance(subsubattr, Attribute)
        True
        >>> subsubattr.get_value()
        'someothervalue'
        """
        if isinstance(attrdict, dict):
            self._config.load(attrdict)
        elif isinstance(attrdict, AttributeSet):
            self._config = attrdict
        else:
            raise AttributeError('Wrong parameter type. Should be a ' + \
                                 'dictionnary or an AttributeSet.')

    def dump(self):
        """
        Dumps the internal configuration dictionnary.
        """
        return self._config.dump()

    def __str__(self):
        """
        Configuration string representation
        """
        return str(self._config)


class MainConfigurationItem(BaseConfigurationItem):
    """
    Main configuration item that contains basic configuration attributes such
    as id, description, reference. It also contains references to sub
    configuration objects representing repository, sites and datagases
    configurations.

    An attribute query method returns an Attribute object. A sub configuration
    query method returns a subclass of BaseConfigurationItem.

    Please see Attribute and AttributeSet objects documentation to have more
    implementation details.
    """

    def __init__(self, attrddict=None):
        """
        Initializes the internal configuration hash
        """
        BaseConfigurationItem.__init__(self, attrddict)

    def get_id(self):
        """
        Returns the configuration identifier (generally the database primary
        key)
        """
        return self.get_attribute('id')

    def get_reference(self):
        """
        Returns the configuration friendly name
        """
        return self.get_attribute('reference')

    def get_description(self):
        """
        Returns the configuration longer description
        """
        return self._config['description']

    def get_repository_configuration(self):
        """
        Returns repository configuration object
        """
        return self.get_attribute('description')

    def get_site_platforms(self, platform):
        """
        Returns the list of knwown site platforms
        """
        sites = self.get_attribute('sites')

        if sites is not None:
            return sites.keys()
        else:
            return []

    def get_site_configuration(self, platform):
        """
        Returns site configuration object for a given platform
        """
        sites = self.get_attribute('sites')

        if sites is not None and sites.has_key(platform):
            return sites[platform]
        else:
            return None

    def get_database_platforms(self, platform):
        """
        Returns the list of knwown database platforms
        """
        databases = self.get_attribute('databases')

        if databases is not None:
            return databases.keys()
        else:
            return []

    def get_database_configuration(self, platform):
        """
        Returns database configuration object for a given platform
        """
        databases = self.get_attribute('databases')

        if databases is not None and databases.has_key(platform):
            return databases[platform]
        else:
            return None

class RepositoryConfigurationItem(BaseConfigurationItem):
    """
    Repository configuration related configuration class.
    """

    def get_type(self):
        """
        Returns repository type (technology: SVN, GIT, ...)
        """
        return self._config['type']

    def get_name(self):
        """
        Returns repository name
        """
        return self._config['name']

    def is_enabled(self):
        """
        Defines whether the repository option has been enabled
        """
        return self._config['enabled']

    def is_done(self):
        """
        Defines whether the repository creation has been handled by a local
        agent
        """
        return self._config['enabled']


class SiteConfigurationItem(BaseConfigurationItem):
    """
    Site configuration related configuration class.
    """

    def get_template(self):
        """
        Returns site template (standard, symfony, ...)
        """
        return self._config['template']

    def get_name(self):
        """
        Returns site name. Default name is reprensetend by the special value
        __DEFAULT__
        """
        return self._config['name']

    def get_domain(self):
        """
        Returns site's DNS domain name.
        """
        return self._config['domain']

    def is_proxied(self):
        """
        Returns site accessibility (True, from internal and externel, False,
        from internal only)
        """
        return self._config['proxied']

    def is_enabled(self):
        """
        Defines whether the repository option has been enabled
        """
        return self._config['enabled']

    def is_done(self):
        """
        Defines whether the repository creation has been handled by a local
        agent
        """
        return self._config['enabled']

class DatabaseConfigurationItem(BaseConfigurationItem):
    """
    Database configuration related configuration class.
    """

    def get_type(self):
        """
        Returns database technology type (MySQL, PostgresQL, ...)
        """
        return self._config['type']

    def get_name(self):
        """
        Returns database name.
        """
        return self._config['name']

    def get_username(self):
        """
        Returns database username used for connection.
        """
        return self._config['username']

    def get_password(self):
        """
        Returns database user password.
        """
        return self._config['password']

    def is_enabled(self):
        """
        Defines whether the repository option has been enabled
        """
        return self._config['enabled']

    def is_done(self):
        """
        Defines whether the repository creation has been handled by a local
        agent
        """
        return self._config['enabled']


###############################################################################

if __name__ == "__main__":
    import doctest
    doctest.testmod()
