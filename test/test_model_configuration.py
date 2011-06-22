#!/usr/bin/env python
"""
Test classes for abstraction.configuration moodule
"""

import unittest
import doctest
from sitebuilder.model import configuration
from sitebuilder.model.configuration import get_checked_default_config
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.utils.attribute import AttributeSet

class Test(unittest.TestCase):
    """
    Unist tests for configuration.
    """

    def test_doctests(self):
        """
        Run configuration doctests
        """
        doctest.testmod(configuration)

    def test_default_configuration(self):
        """
        Tests that default configuration builds correctly and that attributes
        work as expected.
        """
        config = AttributeSet(attributes=get_checked_default_config())

        self.assertEquals(config.get_attribute('id').get_value(), None)
        self.assertEquals(config.get_attribute('reference').get_value(), '')
        self.assertEquals(config.get_attribute('description').get_value(), '')

        repository = config.get_attribute('repository')
        self.assertEquals(repository.get_attribute('enabled').get_value(), False)
        self.assertEquals(repository.get_attribute('done').get_value(), False)
        self.assertEquals(repository.get_attribute('name').get_value(), '')
        self.assertEquals(repository.get_attribute('type').get_value(), 'svn')
        self.assertEquals(repository.get_attribute('type').get_value(), 'svn')
        self.assertTrue(repository.get_attribute('type').get_value() in \
                       ConfigurationManager.get_repository_types())

        sites = config.get_attribute('sites')

        for platform in sites.get_attribute_names():
            site = sites.get_attribute(platform)
            self.assertEquals(site.get_attribute('enabled').get_value(), False)
            self.assertEquals(site.get_attribute('done').get_value(), False)
            self.assertEquals(site.get_attribute('maintenance').get_value(), False)
            self.assertEquals(site.get_attribute('domain').get_value(), 'bpinet.com')
            self.assertTrue(site.get_attribute('domain').get_value() in \
                            ConfigurationManager.get_site_domains())
            self.assertEquals(site.get_attribute('template').get_value(), 'standard')
            self.assertTrue(site.get_attribute('template').get_value() in \
                            ConfigurationManager.get_site_templates())

            if 'proxied' in site.get_attribute_names():
                self.assertEquals(site.get_attribute('proxied').get_value(), False)

        databases = config.get_attribute('databases')

        for platform in databases.get_attribute_names():
            database = databases.get_attribute(platform)
            self.assertEquals(database.get_attribute('enabled').get_value(), False)
            self.assertEquals(database.get_attribute('done').get_value(), False)
            self.assertEquals(database.get_attribute('name').get_value(), '')
            self.assertEquals(database.get_attribute('username').get_value(), '')
            self.assertEquals(database.get_attribute('password').get_value(), '')
            self.assertEquals(database.get_attribute('type').get_value(), 'mysql')
            self.assertTrue(database.get_attribute('type').get_value() in \
                            ConfigurationManager.get_database_types())

    def test_set_configuration(self):
        """
        Tests that configuration attributes react as expected when setting
        attributes value
        """
        config = AttributeSet(attributes=get_checked_default_config())

        _id = config.get_attribute('id')
        _id.set_value(1)
        self.assertEquals(_id.get_value(), 1)
        self.assertRaises(AttributeError, _id.set_value, '1')

        ref = config.get_attribute('reference')
        ref.set_value('ref')
        self.assertEquals(ref.get_value(), 'ref')
        self.assertRaises(AttributeError, ref.set_value, "'")

        desc = config.get_attribute('description')
        desc.set_value('desc')
        self.assertEquals(desc.get_value(), 'desc')
        self.assertRaises(AttributeError, desc.set_value, "'")

        repository = config.get_attribute('repository')

        name = repository.get_attribute('name')
        name.set_value('name')
        self.assertEquals(name.get_value(), 'name')
        self.assertRaises(AttributeError, name.set_value, "'")

        _type = repository.get_attribute('type')
        _type.set_value('git')
        self.assertEquals(_type.get_value(), 'git')
        self.assertRaises(AttributeError, _type.set_value, "type")

        enabled = repository.get_attribute('enabled')
        enabled.set_value(True)
        self.assertEquals(enabled.get_value(), True)
        self.assertRaises(AttributeError, enabled.set_value, 'enabled')

        done = repository.get_attribute('done')
        done.set_value(True)
        self.assertEquals(done.get_value(), True)
        self.assertRaises(AttributeError, done.set_value, 'done')

        sites = config.get_attribute('sites')

        for platform in sites.get_attribute_names():
            site = sites.get_attribute(platform)

            name = site.get_attribute('name')
            name.set_value('name')
            self.assertEquals(name.get_value(), 'name')
            self.assertRaises(AttributeError, name.set_value, "'")

            tmpl = site.get_attribute('template')
            tmpl.set_value('symfony')
            self.assertEquals(tmpl.get_value(), 'symfony')
            self.assertRaises(AttributeError, tmpl.set_value, "fake")

            dom = site.get_attribute('domain')
            dom.set_value('groupe-bpi.com')
            self.assertEquals(dom.get_value(), 'groupe-bpi.com')
            self.assertRaises(AttributeError, dom.set_value, "fake")

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

            if 'proxied' in site.get_attribute_names():
                proxied = site.get_attribute('proxied')
                proxied.set_value(True)
                self.assertEquals(proxied.get_value(), True)
                self.assertRaises(AttributeError, proxied.set_value, 'proxied')

        databases = config.get_attribute('databases')

        for platform in databases.get_attribute_names():
            database = databases.get_attribute(platform)

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
