#!/usr/bin/env python
"""
Site configuration objects related classes
"""

from sitebuilder.utils.attribute import TriggerFieldProperty
from sitebuilder.utils.attribute import UnicodeTriggerFieldProperty
from sitebuilder.abstraction.interface import ISite, IWebsite, IDNSHost
from sitebuilder.abstraction.interface import IDatabase, IRCSRepository
from sitebuilder.event.bus import EventBus
from sitebuilder.event.interface import IEventBroker
from zope.schema.fieldproperty import FieldProperty
from zope.interface import implements


class BaseObject(object):
    """
    Base object to be subclassed by abstraction agents.

    It has an event bus that shoud publish a DataChangedEvent event.
    """

    implements(IEventBroker)

    def __init__(self):
        """
        Object initialization
        """
        self._event_bus = EventBus()

    def get_event_bus(self):
        """
        Returns component's event bus.
        """
        return self._event_bus


class DNSHost(BaseObject):
    """
    DNS configuration description object

    >>> host = DNSHost()
    >>> IDNSHost.providedBy(host)
    True

    >>> class TestObsrver(object):
    ...     notified = False
    ...     def attribute_changed(self, event):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> from sitebuilder.event.events import DataChangeEvent
    >>> observer = TestObsrver()
    >>> host.get_event_bus().subscribe(DataChangeEvent, observer.attribute_changed)
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


class RCSRepository(BaseObject):
    """
    RCS repository configuration description object

    >>> repo = RCSRepository()
    >>> IRCSRepository.providedBy(repo)
    True
    >>> class TestObsrver(object):
    ...     notified = False
    ...     def attribute_changed(self, event):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> from sitebuilder.event.events import DataChangeEvent
    >>> observer = TestObsrver()
    >>> repo.get_event_bus().subscribe(DataChangeEvent, observer.attribute_changed)

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


class Website(BaseObject):
    """
    Site configuration description object

    >>> site = Website()
    >>> IWebsite.providedBy(site)
    True
    >>> class TestObsrver(object):
    ...     notified = False
    ...     def attribute_changed(self, attribute=None):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> from sitebuilder.event.events import DataChangeEvent
    >>> observer = TestObsrver()
    >>> site.get_event_bus().subscribe(DataChangeEvent, observer.attribute_changed)

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


class Database(BaseObject):
    """
    Database configuration description object

    >>> db = Database()
    >>> IDatabase.providedBy(db)
    True
    >>> class TestObsrver(object):
    ...     notified = False
    ...     def attribute_changed(self, attribute=None):
    ...         self.notified = True
    ...

    When observer is set, any  attribute set should call observer

    >>> from sitebuilder.event.events import DataChangeEvent
    >>> observer = TestObsrver()
    >>> db.get_event_bus().subscribe(DataChangeEvent, observer.attribute_changed)

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


class Site(BaseObject):
    """
    Root object describing a whole site configuration.

    It registers itself as observer for suboject describing finer
    configuartions.
    """

    implements(ISite)

    dnshost = TriggerFieldProperty(ISite['dnshost'])
    website = TriggerFieldProperty(ISite['website'])
    repository = TriggerFieldProperty(ISite['repository'])
    database = TriggerFieldProperty(ISite['database'])
    status = FieldProperty(ISite['status'])

    def __init__(self):
        """
        Object initialization
        """
        BaseObject.__init__(self)
        self.dnshost = DNSHost()
        self.dnshost.get_event_bus().connect(self.get_event_bus())

        self.repository = RCSRepository()
        self.repository.get_event_bus().connect(self.get_event_bus())

        self.website = Website()
        self.website.get_event_bus().connect(self.get_event_bus())

        self.database = Database()
        self.database.get_event_bus().connect(self.get_event_bus())


if __name__ == "__main__":
    from zope.schema import getValidationErrors
    from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
    import doctest
    doctest.testmod()
