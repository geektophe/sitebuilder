#!/usr/bin/env python

"""
Site configuration objects related classes
"""

from sitebuilder.abstraction.attribute import TriggerFieldProperty
from sitebuilder.abstraction.attribute import UnicodeTriggerFieldProperty
from sitebuilder.interfaces.site import ISite, IWebsite, IDNSHost, IDatabase
from sitebuilder.interfaces.site import IRCSRepository
from sitebuilder.observer.attribute import AttributeChangedSubject
from sitebuilder.observer.attribute import AttributeChangedObserver
from zope.interface import implements
from zope.schema import getValidationErrors


class DNSHost(AttributeChangedSubject):
    """
    DNS configuration description object

    >>> host = DNSHost()
    >>> IDNSHost.providedBy(host)
    True
    >>> class TestObsrver(AttributeChangedObserver):
    ...     flag = False
    ...     def attribute_changed(self, event=None):
    ...         self.flag = True
    ...

    Name is mandatory and object should not pass shema validation

    >>> getValidationErrors(IDNSHost, host)
    [('name', ConstraintNotSatisfied(u''))]

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> host.register_attribute_changed_observer(observer)
    >>> host.name = 'hostname'
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> host.domain = SiteDefaultsManager.get_default_domain()
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> host.platform = SiteDefaultsManager.get_default_platform()
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> host.done = True
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> host.description = 'desc'
    >>> observer.flag
    True

    Name should contain only alphanumeric characters

    >>> host.name = '@'
    >>> getValidationErrors(IDNSHost, host)
    [('name', ConstraintNotSatisfied(u'@'))]
    >>> host.name = 'allowed'
    >>> getValidationErrors(IDNSHost, host)
    []

    Domain should contain only alloued value

    >>> host.domain = 'fakedomain'
    >>> getValidationErrors(IDNSHost, host)
    [('domain', ConstraintNotSatisfied(u'fakedomain'))]
    >>> host.domain = SiteDefaultsManager.get_default_domain()
    >>> getValidationErrors(IDNSHost, host)
    []

    Platform should contain only alloued value

    >>> host.platform = 'fakeplatform'
    >>> getValidationErrors(IDNSHost, host)
    [('platform', ConstraintNotSatisfied(u'fakeplatform'))]
    >>> host.platform = SiteDefaultsManager.get_default_platform()
    >>> getValidationErrors(IDNSHost, host)
    []

    Done should only be a boolean value

    >>> host.done = 'fake'
    >>> getValidationErrors(IDNSHost, host)
    [('done', WrongType('fake', <type 'bool'>, 'done'))]
    >>> host.done = True
    >>> getValidationErrors(IDNSHost, host)
    []
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
        AttributeChangedSubject.__init__(self)
        # Bypass security to set proper default value
        #self.__dict__['name'] = u''
        #self.__dict__['description '] = u''
        #self.domain = SiteDefaultsManager.get_default_domain()
        #self.platform = SiteDefaultsManager.get_default_platform()
        #self.done = False


class RCSRepository(AttributeChangedSubject):
    """
    RCS repository configuration description object

    >>> repo = RCSRepository()
    >>> IRCSRepository.providedBy(repo)
    True
    >>> class TestObsrver(AttributeChangedObserver):
    ...     flag = False
    ...     def attribute_changed(self, event=None):
    ...         self.flag = True
    ...

    Name is mandatory and object should not pass shema validation

    >>> getValidationErrors(IRCSRepository, repo)
    [('name', ConstraintNotSatisfied(u''))]

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> repo.register_attribute_changed_observer(observer)

    >>> repo.enabled = True
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> repo.name = 'reponame'
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> repo.type = SiteDefaultsManager.get_default_repository_type()
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> repo.done = True
    >>> observer.flag
    True

    Enabled should only be a boolean value

    >>> repo.enabled = 'fake'
    >>> getValidationErrors(IRCSRepository, repo)
    [('enabled', WrongType('fake', <type 'bool'>, 'enabled'))]
    >>> repo.enabled = True
    >>> getValidationErrors(IRCSRepository, repo)
    []

    Name should contain only alphanumeric characters

    >>> repo.name = '@'
    >>> getValidationErrors(IRCSRepository, repo)
    [('name', ConstraintNotSatisfied(u'@'))]
    >>> repo.name = 'allowed'
    >>> getValidationErrors(IRCSRepository, repo)
    []

    Type should contain only alloued value

    >>> repo.type = 'faketype'
    >>> getValidationErrors(IRCSRepository, repo)
    [('type', ConstraintNotSatisfied(u'faketype'))]
    >>> repo.type = SiteDefaultsManager.get_default_repository_type()
    >>> getValidationErrors(IRCSRepository, repo)
    []

    Done should only be a boolean value

    >>> repo.done = 'fake'
    >>> getValidationErrors(IRCSRepository, repo)
    [('done', WrongType('fake', <type 'bool'>, 'done'))]
    >>> repo.done = True
    >>> getValidationErrors(IRCSRepository, repo)
    []
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
        AttributeChangedSubject.__init__(self)
        # Bypass security to set proper default value
        #self.__dict__['name'] = u''
        #self.enabled = False
        #self.type = SiteDefaultsManager.get_default_repository_type()
        #self.done = False


class Website(AttributeChangedSubject):
    """
    Site configuration description object

    >>> site = Website()
    >>> IWebsite.providedBy(site)
    True
    >>> class TestObsrver(AttributeChangedObserver):
    ...     flag = False
    ...     def attribute_changed(self, event=None):
    ...         self.flag = True
    ...

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> site.register_attribute_changed_observer(observer)

    >>> site.enabled = True
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> site.maintenance = True
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> site.access = SiteDefaultsManager.get_default_site_access()
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> site.template = SiteDefaultsManager.get_default_site_template()
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> site.done = True
    >>> observer.flag
    True

    Enabled should only be a boolean value

    >>> site.enabled = 'fake'
    >>> getValidationErrors(IWebsite, site)
    [('enabled', WrongType('fake', <type 'bool'>, 'enabled'))]
    >>> site.enabled = True
    >>> getValidationErrors(IWebsite, site)
    []

    Maintenance should only be a boolean value

    >>> site.maintenance = 'fake'
    >>> getValidationErrors(IWebsite, site)
    [('maintenance', WrongType('fake', <type 'bool'>, 'maintenance'))]
    >>> site.maintenance = True
    >>> getValidationErrors(IWebsite, site)
    []

    Access should contain only alloued value

    >>> site.access = 'fakeaccess'
    >>> getValidationErrors(IWebsite, site)
    [('access', ConstraintNotSatisfied(u'fakeaccess'))]
    >>> site.access = SiteDefaultsManager.get_default_site_access()
    >>> getValidationErrors(IWebsite, site)
    []

    Access should contain only alloued value

    >>> site.template = 'faketemplate'
    >>> getValidationErrors(IWebsite, site)
    [('template', ConstraintNotSatisfied(u'faketemplate'))]
    >>> site.template = SiteDefaultsManager.get_default_site_template()
    >>> getValidationErrors(IWebsite, site)
    []

    Done should only be a boolean value

    >>> site.done = 'fake'
    >>> getValidationErrors(IWebsite, site)
    [('done', WrongType('fake', <type 'bool'>, 'done'))]
    >>> site.done = True
    >>> getValidationErrors(IWebsite, site)
    []
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
        AttributeChangedSubject.__init__(self)
        #self.enabled = False
        #self.template = SiteDefaultsManager.get_default_site_template()
        #self.access = SiteDefaultsManager.get_default_site_access()
        #self.maintenance = False
        #self.done = False


class Database(AttributeChangedSubject):
    """
    Database configuration description object

    >>> db = Database()
    >>> IDatabase.providedBy(db)
    True
    >>> class TestObsrver(AttributeChangedObserver):
    ...     flag = False
    ...     def attribute_changed(self, event=None):
    ...         self.flag = True
    ...

    Name and username are mandatory and object should not pass shema validation

    >>> getValidationErrors(IDatabase, db)
    [('username', ConstraintNotSatisfied(u'')), ('name', ConstraintNotSatisfied(u''))]

    When observer is set, any  attribute set should call observer

    >>> observer = TestObsrver()
    >>> db.register_attribute_changed_observer(observer)

    >>> db.enabled = True
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> db.name = 'dbname'
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> db.username = 'dbusername'
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> db.password = 'dbpassword'
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> db.type = SiteDefaultsManager.get_default_database_type()
    >>> observer.flag
    True

    >>> observer.flag = False
    >>> db.done = True
    >>> observer.flag
    True

    Enabled should only be a boolean value

    >>> db.enabled = 'fake'
    >>> getValidationErrors(IDatabase, db)
    [('enabled', WrongType('fake', <type 'bool'>, 'enabled'))]
    >>> db.enabled = True
    >>> getValidationErrors(IDatabase, db)
    []

    Name should contain only alphanumeric characters

    >>> db.name = '@'
    >>> getValidationErrors(IDatabase, db)
    [('name', ConstraintNotSatisfied(u'@'))]
    >>> db.name = 'allowed'
    >>> getValidationErrors(IDatabase, db)
    []

    Username should contain only alphanumeric characters

    >>> db.username = '@'
    >>> getValidationErrors(IDatabase, db)
    [('username', ConstraintNotSatisfied(u'@'))]
    >>> db.username = 'allowed'
    >>> getValidationErrors(IDatabase, db)
    []

    Type should contain only alloued value

    >>> db.type = 'faketype'
    >>> getValidationErrors(IDatabase, db)
    [('type', ConstraintNotSatisfied(u'faketype'))]
    >>> db.type = SiteDefaultsManager.get_default_database_type()
    >>> getValidationErrors(IDatabase, db)
    []

    Done should only be a boolean value

    >>> db.done = 'fake'
    >>> getValidationErrors(IDatabase, db)
    [('done', WrongType('fake', <type 'bool'>, 'done'))]
    >>> db.done = True
    >>> getValidationErrors(IDatabase, db)
    []
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
        AttributeChangedSubject.__init__(self)
        # Bypass security to set proper default value
        #self.__dict__['name'] = u''
        #self.__dict__['username'] = u''
        #self.__dict__['password'] = u''
        #self.enabled = False
        #self.type = SiteDefaultsManager.get_default_database_type()
        #self.done = False


class Site(AttributeChangedSubject, AttributeChangedObserver):
    """
    Root object describing a whole site configuration.

    It registers itself as observer for suboject describing finer
    configuartions.
    """

    implements(ISite)

    def __init__(self):
        """
        Object initialization
        """
        AttributeChangedSubject.__init__(self)

        self.dnshost = DNSHost()
        self.dnshost.register_attribute_changed_observer(self)

        self.repository = RCSRepository()
        self.repository.register_attribute_changed_observer(self)

        self.website = Website()
        self.website.register_attribute_changed_observer(self)

        self.database = Database()
        self.database.register_attribute_changed_observer(self)

    def attribute_changed(self, event=None):
        """
        Notifies all observers that upper attribute has changed
        """
        self.notify_attribute_changed(event)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
