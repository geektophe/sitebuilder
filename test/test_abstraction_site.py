#!/usr/bin/env python
"""
Test classes for abstraction.site moodule
"""

import unittest
import doctest
from sitebuilder.utils.parameters import set_application_context
from sitebuilder.abstraction.site import manager
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.abstraction.site.manager import SiteConfigurationManager
from zope.schema import ValidationError

class Test(unittest.TestCase):
    """
    Unist tests for site.
    """

    def setUp(self):
        """
        Enables test context
        """
        set_application_context('test')

    def test_doctests(self):
        """
        Run site doctests
        """
        doctest.testmod(manager)

    def test_default_site(self):
        """
        Tests that default site builds correctly and that attributes
        work as expected.
        """
        config = SiteConfigurationManager.get_blank_site()

        dnshost = config.dnshost
        self.assertEquals(dnshost.domain,
                          SiteDefaultsManager.get_default_domain())
        self.assertEquals(dnshost.name, u'')
        self.assertEquals(dnshost.platform,
                          SiteDefaultsManager.get_default_platform())
        self.assertTrue(dnshost.platform in \
                       SiteDefaultsManager.get_platforms())
        self.assertEquals(dnshost.description, u'')

        repository = config.repository
        self.assertEquals(repository.enabled, False)
        self.assertEquals(repository.done, False)
        self.assertEquals(repository.name, u'')
        self.assertEquals(repository.type,
                          SiteDefaultsManager.get_default_repository_type())
        self.assertTrue(repository.type in \
                       SiteDefaultsManager.get_repository_types())

        site = config.website
        self.assertEquals(site.enabled, False)
        self.assertEquals(site.done, False)
        self.assertEquals(site.maintenance, False)
        self.assertEquals(site.template,
                          SiteDefaultsManager.get_default_site_template())
        self.assertTrue(site.template in \
                        SiteDefaultsManager.get_site_templates())
        self.assertEquals(site.access,
                          SiteDefaultsManager.get_default_site_access())
        self.assertTrue(site.access in \
                        SiteDefaultsManager.get_site_accesses())

        database = config.database
        self.assertEquals(database.enabled, False)
        self.assertEquals(database.done, False)
        self.assertEquals(database.name, u'')
        self.assertEquals(database.username, u'')
        self.assertEquals(database.password, u'')
        self.assertEquals(database.type,
                          SiteDefaultsManager.get_default_database_type())
        self.assertTrue(database.type in \
                        SiteDefaultsManager.get_database_types())

    def test_set_site(self):
        """
        Tests that site attributes react as expected when setting
        attributes value
        """
        config = SiteConfigurationManager.get_blank_site()

        # DNS Host attributes
        dnshost = config.dnshost
        dnshost.desc = 'desc'
        self.assertEquals(dnshost.desc, 'desc')

        dnshost.name = 'name'
        self.assertEquals(dnshost.name, 'name')
        self.assertRaises(ValidationError, lambda x: setattr(dnshost, 'name', x), "f@ke")

        dnshost.domain = SiteDefaultsManager.get_default_domain()
        self.assertEquals(dnshost.domain, SiteDefaultsManager.get_default_domain())
        self.assertRaises(ValidationError, lambda x: setattr(dnshost, 'domain', x), "fake")

        # Repository related attributes
        repository = config.repository

        repository.name = 'name'
        self.assertEquals(repository.name, 'name')
        self.assertRaises(ValidationError, lambda x: setattr(repository, 'name', x), "f@ke")

        repository.type = SiteDefaultsManager.get_default_repository_type()
        self.assertEquals(repository.type,
                          SiteDefaultsManager.get_default_repository_type())
        self.assertRaises(ValidationError, lambda x: setattr(repository, 'type', x), "fake")

        repository.enabled = True
        self.assertEquals(repository.enabled, True)
        self.assertRaises(ValidationError, lambda x: setattr(repository, 'enabled', x), 'fake')

        repository.done = True
        self.assertEquals(repository.done, True)
        self.assertRaises(ValidationError, lambda x: setattr(repository, 'done', x), 'fake')

        # Web site related attributes
        site = config.website

        site.template = SiteDefaultsManager.get_default_site_template()
        self.assertEquals(site.template,
                          SiteDefaultsManager.get_default_site_template())
        self.assertRaises(ValidationError, lambda x: setattr(repository, 'done', x), "fake")

        site.access = SiteDefaultsManager.get_default_site_access()
        self.assertEquals(site.access,
                          SiteDefaultsManager.get_default_site_access())
        self.assertRaises(ValidationError, lambda x: setattr(repository, 'done', x), "fake")

        site.maintenance = True
        self.assertEquals(site.maintenance, True)
        self.assertRaises(ValidationError, lambda x: setattr(site, 'maintenance', x), 'fake')

        site.enabled = True
        self.assertEquals(site.enabled, True)
        self.assertRaises(ValidationError, lambda x: setattr(site, 'enabled', x), 'fake')

        site.done = True
        self.assertEquals(site.done, True)
        self.assertRaises(ValidationError, lambda x: setattr(site, 'done', x), 'fake')

        # Database related attribute
        database = config.database

        database.type = SiteDefaultsManager.get_default_database_type()
        self.assertEquals(database.type,
                          SiteDefaultsManager.get_default_database_type())
        self.assertRaises(ValidationError, lambda x: setattr(repository, 'done', x), "fake")

        database.name = 'name'
        self.assertEquals(database.name, 'name')
        self.assertRaises(ValidationError, lambda x: setattr(database, 'name', x), "f@ke")

        database.username = 'username'
        self.assertEquals(database.username, 'username')
        self.assertRaises(ValidationError, lambda x: setattr(database, 'username', x), "f@ke")

        database.password = 'password'
        self.assertEquals(database.password, 'password')

        database.enabled = True
        self.assertEquals(database.enabled, True)
        self.assertRaises(ValidationError, lambda x: setattr(database, 'enabled', x), 'fake')

        database.done = True
        self.assertEquals(database.done, True)
        self.assertRaises(ValidationError, lambda x: setattr(database, 'done', x), 'fake')


if __name__ == "__main__":
    unittest.main()
