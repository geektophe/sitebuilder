#!/usr/bin/env python
"""
Test classes for abstraction.configuration moodule
"""

import unittest
import doctest
from sitebuilder.utils.parameters import set_application_context
from sitebuilder.abstraction import site
from sitebuilder.abstraction.site import SiteConfigurationManager

class Test(unittest.TestCase):
    """
    Unist tests for configuration.
    """

    def setUp(self):
        """
        Enables test context
        """
        set_application_context('test')

    def test_doctests(self):
        """
        Run configuration doctests
        """
        doctest.testmod(site)

    def test_default_configuration(self):
        """
        Tests that default configuration builds correctly and that attributes
        work as expected.
        """
        config = SiteConfigurationManager.get_blank_configuration()

        general = config.get_attribute('general')
        self.assertEquals(general.get_attribute('id').get_value(), None)
        self.assertEquals(general.get_attribute('domain').get_value(),
                          SiteConfigurationManager.get_default_domain())
        self.assertEquals(general.get_attribute('name').get_value(), '')
        self.assertEquals(general.get_attribute('platform').get_value(),
                          SiteConfigurationManager.get_default_platform())
        self.assertTrue(general.get_attribute('platform').get_value() in \
                       SiteConfigurationManager.get_platforms())
        self.assertEquals(general.get_attribute('description').get_value(), '')

        repository = config.get_attribute('repository')
        self.assertEquals(repository.get_attribute('enabled').get_value(), False)
        self.assertEquals(repository.get_attribute('done').get_value(), False)
        self.assertEquals(repository.get_attribute('name').get_value(), '')
        self.assertEquals(repository.get_attribute('type').get_value(),
                          SiteConfigurationManager.get_default_repository_type())
        self.assertTrue(repository.get_attribute('type').get_value() in \
                       SiteConfigurationManager.get_repository_types())

        site = config.get_attribute('website')
        self.assertEquals(site.get_attribute('enabled').get_value(), False)
        self.assertEquals(site.get_attribute('done').get_value(), False)
        self.assertEquals(site.get_attribute('maintenance').get_value(), False)
        self.assertEquals(site.get_attribute('template').get_value(),
                          SiteConfigurationManager.get_default_site_template())
        self.assertTrue(site.get_attribute('template').get_value() in \
                        SiteConfigurationManager.get_site_templates())
        self.assertEquals(site.get_attribute('access').get_value(),
                          SiteConfigurationManager.get_default_access())
        self.assertTrue(site.get_attribute('access').get_value() in \
                        SiteConfigurationManager.get_accesses())

        database = config.get_attribute('database')
        self.assertEquals(database.get_attribute('enabled').get_value(), False)
        self.assertEquals(database.get_attribute('done').get_value(), False)
        self.assertEquals(database.get_attribute('name').get_value(), '')
        self.assertEquals(database.get_attribute('username').get_value(), '')
        self.assertEquals(database.get_attribute('password').get_value(), '')
        self.assertEquals(database.get_attribute('type').get_value(),
                          SiteConfigurationManager.get_default_database_type())
        self.assertTrue(database.get_attribute('type').get_value() in \
                        SiteConfigurationManager.get_database_types())

    def test_set_configuration(self):
        """
        Tests that configuration attributes react as expected when setting
        attributes value
        """
        config = SiteConfigurationManager.get_blank_configuration()

        # General attributes
        general = config.get_attribute('general')
        _id = general.get_attribute('id')
        _id.set_value(1)
        self.assertEquals(_id.get_value(), 1)
        self.assertRaises(AttributeError, _id.set_value, '1')

        desc = general.get_attribute('description')
        desc.set_value('desc')
        self.assertEquals(desc.get_value(), 'desc')

        name = general.get_attribute('name')
        name.set_value('name')
        self.assertEquals(name.get_value(), 'name')
        self.assertRaises(AttributeError, name.set_value, "'")

        dom = general.get_attribute('domain')
        dom.set_value(SiteConfigurationManager.get_default_domain())
        self.assertEquals(dom.get_value(),
                          SiteConfigurationManager.get_default_domain())
        self.assertRaises(AttributeError, dom.set_value, "fake")

        # Repository related attributes
        repository = config.get_attribute('repository')

        name = repository.get_attribute('name')
        name.set_value('name')
        self.assertEquals(name.get_value(), 'name')
        self.assertRaises(AttributeError, name.set_value, " fake ")

        _type = repository.get_attribute('type')
        _type.set_value(SiteConfigurationManager.get_default_repository_type())
        self.assertEquals(_type.get_value(),
                          SiteConfigurationManager.get_default_repository_type())
        self.assertRaises(AttributeError, _type.set_value, "fake")

        enabled = repository.get_attribute('enabled')
        enabled.set_value(True)
        self.assertEquals(enabled.get_value(), True)
        self.assertRaises(AttributeError, enabled.set_value, 'fake')

        done = repository.get_attribute('done')
        done.set_value(True)
        self.assertEquals(done.get_value(), True)
        self.assertRaises(AttributeError, done.set_value, 'fake')


        # Web site related attributes
        site = config.get_attribute('website')

        tmpl = site.get_attribute('template')
        tmpl.set_value(SiteConfigurationManager.get_default_site_template())
        self.assertEquals(tmpl.get_value(),
                          SiteConfigurationManager.get_default_site_template())
        self.assertRaises(AttributeError, tmpl.set_value, "fake")

        access = site.get_attribute('access')
        access.set_value(SiteConfigurationManager.get_default_access())
        self.assertEquals(access.get_value(),
                          SiteConfigurationManager.get_default_access())
        self.assertRaises(AttributeError, access.set_value, "fake")

        enabled = site.get_attribute('enabled')
        enabled.set_value(True)
        self.assertEquals(enabled.get_value(), True)
        self.assertRaises(AttributeError, enabled.set_value, 'enabled')

        done = site.get_attribute('done')
        done.set_value(True)
        self.assertEquals(done.get_value(), True)
        self.assertRaises(AttributeError, done.set_value, 'done')

        maint = site.get_attribute('maintenance')
        maint.set_value(True)
        self.assertEquals(maint.get_value(), True)
        self.assertRaises(AttributeError, maint.set_value, "maintenance")

        # Database related attribute
        database = config.get_attribute('database')

        _type = database.get_attribute('type')
        _type.set_value(SiteConfigurationManager.get_default_database_type())
        self.assertEquals(_type.get_value(),
                          SiteConfigurationManager.get_default_database_type())
        self.assertRaises(AttributeError, _type.set_value, "fake")

        name = database.get_attribute('name')
        name.set_value('name')
        self.assertEquals(name.get_value(), 'name')
        self.assertRaises(AttributeError, name.set_value, "'")

        username = database.get_attribute('username')
        username.set_value('username')
        self.assertEquals(username.get_value(), 'username')
        self.assertRaises(AttributeError, username.set_value, "'")

        password = database.get_attribute('password')
        password.set_value('password')
        self.assertEquals(password.get_value(), 'password')

        enabled = database.get_attribute('enabled')
        enabled.set_value(True)
        self.assertEquals(enabled.get_value(), True)
        self.assertRaises(AttributeError, enabled.set_value, 'enabled')

        done = database.get_attribute('done')
        done.set_value(True)
        self.assertEquals(done.get_value(), True)
        self.assertRaises(AttributeError, done.set_value, 'done')


if __name__ == "__main__":
    unittest.main()
