#!/usr/bin/env python
"""
Site configuration objects related classes
"""

from sitebuilder.utils.attribute import TriggerFieldProperty
from sitebuilder.utils.attribute import UnicodeTriggerFieldProperty
from sitebuilder.abstraction.interface import ISite, IWebsite, IDNSHost
from sitebuilder.abstraction.interfae import IDatabase, IRCSRepository
from sitebuilder.observer.attribute import IAttributeObserver, AttributeSubject
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema import getValidationErrors


class DNSHost(AttributeSubject):
    """
    DNS configuration description object

    >>> host = DNSHost()
    >>> IDNSHost.providedBy(host)
    True
    >>> class TestObsrver(object):
    ...     implements(IAttributeObserver)
    ...     notified = False
    ...     def attribute_changed(self, attribute=None):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> host.register_attribute_observer(observer)
    >>> host.name = u'hostname'
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> host.domain = SiteDefaultsManager.get_default_domain()
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> host.platform = SiteDefaultsManager.get_default_platform()
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> host.done = True
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> host.description = u'desc'
    >>> observer.notified
    True
    """
    implements(IDNSHost)

    name = UnicodeTriggerFieldProperty(IDNSHost['name'])
    domain = UnicodeTriggerFieldProperty(IDNSHost['domain'])
    platform = UnicodeTriggerFieldProperty(IDNSHost['platform'])
    description = UnicodeTriggerFieldProperty(IDNSHost['description'])
    done = TriggerFieldProperty(IDNSHost['done'])

    def __init__(self):
        """
        Object initialization
        """
        AttributeSubject.__init__(self)


class RCSRepository(AttributeSubject):
    """
    RCS repository configuration description object

    >>> repo = RCSRepository()
    >>> IRCSRepository.providedBy(repo)
    True
    >>> class TestObsrver(object):
    ...     implements(IAttributeObserver)
    ...     notified = False
    ...     def attribute_changed(self, attribute=None):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> repo.register_attribute_observer(observer)

    >>> repo.enabled = True
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> repo.name = u'reponame'
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> repo.type = SiteDefaultsManager.get_default_repository_type()
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> repo.done = True
    >>> observer.notified
    True
    """
    implements(IRCSRepository)

    enabled = TriggerFieldProperty(IRCSRepository['enabled'])
    name = UnicodeTriggerFieldProperty(IRCSRepository['name'])
    type = UnicodeTriggerFieldProperty(IRCSRepository['type'])
    done = TriggerFieldProperty(IRCSRepository[u'done'])

    def __init__(self):
        """
        Object initialization
        """
        AttributeSubject.__init__(self)


class Website(AttributeSubject):
    """
    Site configuration description object

    >>> site = Website()
    >>> IWebsite.providedBy(site)
    True
    >>> class TestObsrver(object):
    ...     implements(IAttributeObserver)
    ...     notified = False
    ...     def attribute_changed(self, attribute=None):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> site.register_attribute_observer(observer)

    >>> site.enabled = True
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> site.maintenance = True
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> site.access = SiteDefaultsManager.get_default_site_access()
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> site.template = SiteDefaultsManager.get_default_site_template()
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> site.done = True
    >>> observer.notified
    True
    """
    implements(IWebsite)

    enabled = TriggerFieldProperty(IWebsite['enabled'])
    template = UnicodeTriggerFieldProperty(IWebsite['template'])
    access = UnicodeTriggerFieldProperty(IWebsite['access'])
    maintenance = TriggerFieldProperty(IWebsite['maintenance'])
    done = TriggerFieldProperty(IWebsite['done'])

    def __init__(self):
        """
        Object initialization
        """
        AttributeSubject.__init__(self)


class Database(AttributeSubject):
    """
    Database configuration description object

    >>> db = Database()
    >>> IDatabase.providedBy(db)
    True
    >>> class TestObsrver(object):
    ...     implements(IAttributeObserver)
    ...     notified = False
    ...     def attribute_changed(self, attribute=None):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> db.register_attribute_observer(observer)

    >>> db.enabled = True
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> db.name = u'dbname'
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> db.username = u'dbusername'
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> db.password = u'dbpassword'
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> db.type = SiteDefaultsManager.get_default_database_type()
    >>> observer.notified
    True

    >>> observer.notified = False
    >>> db.done = True
    >>> observer.notified
    True
    """
    implements(IDatabase)

    enabled = TriggerFieldProperty(IDatabase['enabled'])
    type = UnicodeTriggerFieldProperty(IDatabase['type'])
    name = UnicodeTriggerFieldProperty(IDatabase['name'])
    username = UnicodeTriggerFieldProperty(IDatabase['username'])
    password = UnicodeTriggerFieldProperty(IDatabase['password'])
    done = TriggerFieldProperty(IDatabase['done'])

    def __init__(self):
        """
        Object initialization
        """
        AttributeSubject.__init__(self)
        # Bypass security to set proper default value
        #self.__dict__['name'] = u''
        #self.__dict__['username'] = u''
        #self.__dict__['password'] = u''
        #self.enabled = False
        #self.type = SiteDefaultsManager.get_default_database_type()
        #self.done = False


class Site(AttributeSubject):
    """
    Root object describing a whole site configuration.

    It registers itself as observer for suboject describing finer
    configuartions.
    """

    implements(ISite, IAttributeObserver)

    dnshost = TriggerFieldProperty(ISite['dnshost'])
    website = TriggerFieldProperty(ISite['website'])
    repository = TriggerFieldProperty(ISite['repository'])
    database = TriggerFieldProperty(ISite['database'])
    status = FieldProperty(ISite['status'])

    def __init__(self):
        """
        Object initialization
        """
        AttributeSubject.__init__(self)

        self.dnshost = DNSHost()
        self.dnshost.register_attribute_observer(self)

        self.repository = RCSRepository()
        self.repository.register_attribute_observer(self)

        self.website = Website()
        self.website.register_attribute_observer(self)

        self.database = Database()
        self.database.register_attribute_observer(self)

    def attribute_changed(self, attribute=None):
        """
        Notifies all observers that upper attribute has changed
        """
        self.notify_attribute_changed(attribute)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
