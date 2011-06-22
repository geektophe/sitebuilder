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

if __name__ == "__main__":
    unittest.main()
