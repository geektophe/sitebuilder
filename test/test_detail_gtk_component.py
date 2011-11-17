#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
from sitebuilder.utils.parameters import set_application_context
from sitebuilder.abstraction.site.manager import SiteConfigurationManager
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.control.detail import DetailSiteControlAgent
from sitebuilder.control.detail import DetailDatabaseControlAgent
from sitebuilder.control.detail import DetailRepositoryControlAgent
from sitebuilder.control.detail import DetailDNSHostControlAgent


class BaseTestGtkPresentationAgent(unittest.TestCase):
    """Unit test base class to be subclassed by real test cases"""

    def setUp(self):
        """
        Enables test context
        """
        set_application_context('test')

    def assert_widgets_active_flag(self, presentation_agent, flags):
        """
        Checks that widgets active flag is set as of values dctionnary
        configuraiton.
        """
        for name, flag in flags.items():
            self.assertEquals(presentation_agent[name].get_active(), flag,
                    "%s widget active flag sould be %s" % (name, flag))

    def assert_widgets_sensitive_flag(self, presentation_agent, flags):
        """
        Checks that widgets active flag is set as of values dctionnary
        configuraiton.
        """

        for name, flag in flags.items():
            self.assertEquals(presentation_agent[name].get_sensitive(), flag,
                    "%s widget sensitive flag sould be %s" % (name, flag))


class TestDetailSiteGtkPresentationAgent(BaseTestGtkPresentationAgent):
    """Unit tests for site detail gtk presentation_agents"""

    def detail_website_state_test(self, website):
        """
        Tests site detail component's presentation_agent initial state
        """
        control_agent = DetailSiteControlAgent(website)
        presentation_agent = control_agent.get_presentation_agent()
        done = website.done
        enabled = website.enabled
        refresh_gui()

        # Tests checkboxes state
        flags = {
            'enabled': enabled,
            'maintenance': website.maintenance
            }
        self.assert_widgets_active_flag(presentation_agent, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not done,
            'maintenance': enabled,
            'template': not done and enabled,
            'access': enabled,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_website_init_state(self):
        """
        Tests site detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config.website
        self.detail_website_state_test(website)

    def test_detail_website_enabled_state(self):
        """
        Tests site detail component's presentation_agent in done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config.website
        website.enabled = True
        self.detail_website_state_test(website)

    def test_detail_website_done_state(self):
        """
        Tests site detail component's presentation_agent in done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config.website
        website.enabled = True
        website.done = True
        self.detail_website_state_test(website)

    def test_detail_website_gui_actions(self):
        """
        Tests that site detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config.website
        control_agent = DetailSiteControlAgent(website)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Enables component
        presentation_agent['enabled'].set_active(True)
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'enabled': True,
            'maintenance': True,
            'template': True,
            'access': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # When a checkbox is enabled, the corresponding attribute should follow
        for name in ('enabled', 'maintenance'):
            presentation_agent[name].set_active(True)
            refresh_gui()
            self.assertTrue(getattr(website, name),
                            'site %s attribute is not enabled' % name)

        # Comboboxes value should be reported to abstraction
        template = SiteDefaultsManager.get_site_templates().keys()[0]
        access = SiteDefaultsManager.get_site_accesses().keys()[0]

        for name, value in {'template': template, 'access': access}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(getattr(website, name), value,
                             'site %s attribute is wrong' % name)

    def test_detail_website_abstraction_actions(self):
        """
        Tests that site detail component's abstractions changes are correctly
        reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config.website
        control_agent = DetailSiteControlAgent(website)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Enables component
        website.enabled = True
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'enabled': True,
            'maintenance': True,
            'template': True,
            'access': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # When a widget is enabled, the corresponding attribute should follow
        for name in ('enabled', 'maintenance'):
            setattr(website, name, True)
            refresh_gui()
            self.assert_widgets_active_flag(presentation_agent, {name: True})

        # Comboboxes value should reflect abstraction changes
        template = SiteDefaultsManager.get_site_templates().keys()[0]
        access = SiteDefaultsManager.get_site_accesses().keys()[0]

        for name, value in {'template': template, 'access': access}.items():
            setattr(website, name, value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'site %s: %s/%s widget selection is wrong' % (name, value, presentation_agent.get_combobox_selection(presentation_agent[name])))

        # Tests that when done flag is set, sentivity is disabled on enabled
        # and template widgets. Maintenance and access should remain sensitive
        website.done = True
        refresh_gui()

        # Tests final widgets sensitivity
        flags = {
            'enabled': False,
            'template': False,
            'maintenance': True,
            'access': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_website_read_only(self):
        """
        Tests that site detail component's abstractions changes are correctly
        reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config.website
        control_agent = DetailSiteControlAgent(website, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'enabled': False,
            'maintenance': False,
            'template': False,
            'access': False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)


class TestDetailDatabaseGtkPresentationAgent(BaseTestGtkPresentationAgent):
    """Unit tests for database detail gtk presentation_agents"""

    def detail_database_state_test(self, database):
        """
        Tests site detail component's presentation_agent initial state
        """
        done = database.done
        enabled = database.enabled
        control_agent = DetailDatabaseControlAgent(database)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests checkboxes state
        flags = { 'enabled': enabled }
        self.assert_widgets_active_flag(presentation_agent, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not done,
            'name': enabled and not done,
            'username': enabled and not done,
            'password': enabled and not done,
            'type': enabled and not done,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_database_init_state(self):
        """
        Tests site detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config.database
        self.detail_database_state_test(database)

    def test_detail_database_enabled_state(self):
        """
        Tests site detail component's presentation_agent n done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config.database
        database.enabled = True
        self.detail_database_state_test(database)

    def test_detail_database_done_state(self):
        """
        Tests site detail component's presentation_agent n done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config.database
        database.enabled = True
        database.done = True
        self.detail_database_state_test(database)

    def test_detail_database_gui_actions(self):
        """
        Tests that database detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config.database
        control_agent = DetailDatabaseControlAgent(database)
        presentation_agent = control_agent.get_presentation_agent()
        presentation_agent['enabled'].set_active(True)
        refresh_gui()

        # Enables component
        presentation_agent['enabled'].set_active(True)
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'enabled': True,
            'type': True,
            'name': True,
            'username': True,
            'password': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # When a widget is enabled, the corresponding attribute should follow
        for name in ('enabled',):
            setattr(database, name, True)
            refresh_gui()
            self.assert_widgets_active_flag(presentation_agent, {name: True})

        # When an entry is set, the abstraction should have corresponding
        # value set
        for name in ('name', 'username', 'password'):
            presentation_agent[name].set_text('abc')
            refresh_gui()
            self.assertEquals(getattr(database, name), 'abc',
                             'database %s attribute is wrong' % name)

        # Comboboxes value should be reported to abstraction
        dbtype = SiteDefaultsManager.get_database_types().keys()[0]

        for name, value in {'type': dbtype}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(getattr(database, name), value,
                             'site %s attribute is wrong' % name)

    def test_detail_database_abstraction_actions(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config.database
        control_agent = DetailDatabaseControlAgent(database)
        presentation_agent = control_agent.get_presentation_agent()
        database.enabled = True
        refresh_gui()

        # All widgets should be enabled
        flags = {
            'enabled': True,
            'type': True,
            'name': True,
            'username': True,
            'password': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(presentation_agent, {'enabled': True})

        # When a name, username or password is set, correpsonding widget
        # should follow
        for name in ('name', 'username', 'password'):
            setattr(database, name, 'abc')
            refresh_gui()
            self.assertEquals(presentation_agent[name].get_text(), 'abc',
                             'database %s widget is wrong' % name)

        # Comboboxes value should reflect abstraction changes
        dbtype = SiteDefaultsManager.get_database_types().keys()[0]

        for name, value in {'type': dbtype}.items():
            setattr(database, name, value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'database %s widget selection is wrong' % name)

        # Tests that when done flag is set, allw widgets are disabled
        database.done = True
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'enabled': False,
            'type': False,
            'name': False,
            'username': False,
            'password': False,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_database_read_only(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config.database
        control_agent = DetailDatabaseControlAgent(database, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'enabled': False,
            'name':  False,
            'username':  False,
            'password':  False,
            'type':  False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_database_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config.database
        control_agent = DetailDatabaseControlAgent(database, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        database.enabled = True
        refresh_gui()

        for widget in ('name', 'username'):
            presentation_agent[widget].set_text('abc')
            refresh_gui()
            self.assertTrue(presentation_agent.get_validity_flag(),
                            'database validity should be true')

            presentation_agent[widget].set_text('ab c')
            refresh_gui()
            self.assertFalse(presentation_agent.get_validity_flag(),
                            'database validity should be false')


class TestDetailRepositoryGtkPresentationAgent(BaseTestGtkPresentationAgent):
    """Unit tests for repository detail gtk presentation_agents"""

    def detail_repository_state_test(self, repo):
        """
        Tests repo detail component's presentation_agent state
        """
        control_agent = DetailRepositoryControlAgent(repo)
        presentation_agent = control_agent.get_presentation_agent()
        done = repo.done
        enabled = repo.enabled
        refresh_gui()

        # Tests checkboxes state
        flags = {
            'enabled': enabled,
            }
        self.assert_widgets_active_flag(presentation_agent, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not done,
            'type': not done and enabled,
            'name': not done and enabled,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_repository_init_state(self):
        """
        Tests repo detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config.repository
        self.detail_repository_state_test(repo)

    def test_detail_repository_enabled_state(self):
        """
        Tests repo detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config.repository
        repo.enabled = True
        self.detail_repository_state_test(repo)

    def test_detail_repository_done_state(self):
        """
        Tests repo detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config.repository
        repo.enabled = True
        repo.done = True
        self.detail_repository_state_test(repo)

    def test_detail_repository_gui_actions(self):
        """
        Tests that repo detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config.repository
        control_agent = DetailRepositoryControlAgent(repo)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Enables component
        presentation_agent['enabled'].set_active(True)
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'enabled': True,
            'type': True,
            'name': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # When a checkbox is enabled, the corresponding attribute should follow
        for name in ('enabled',):
            presentation_agent[name].set_active(True)
            refresh_gui()
            self.assertTrue(getattr(repo, name),
                            'repo %s attribute is not enabled' % name)

        # Comboboxes value should be reported to abstraction
        repotype = SiteDefaultsManager.get_repository_types().keys()[0]

        for name, value in {'type': repotype}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(getattr(repo, name), value,
                             'repo %s attribute is wrong' % name)

    def test_detail_repository_abstraction_actions(self):
        """
        Tests that repo detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config.repository
        control_agent = DetailRepositoryControlAgent(repo)
        presentation_agent = control_agent.get_presentation_agent()
        repo.enabled = True
        refresh_gui()

        # All widgets should be enabled
        flags = {
            'enabled': True,
            'type': True,
            'name': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(presentation_agent, {'enabled': True})

        # When a name, username or password is set, correpsonding widget
        # should follow
        for name in ('name',):
            setattr(repo, name, 'abc')
            refresh_gui()
            self.assertEquals(presentation_agent[name].get_text(), 'abc',
                             'repo %s widget is wrong' % name)

        # Comboboxes value should reflect abstraction changes
        repotype = SiteDefaultsManager.get_repository_types().keys()[0]

        for name, value in {'type': repotype}.items():
            setattr(repo, name, value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'repo %s widget selection is wrong' % name)

        # Tests that when done flag is set, allw widgets are disabled
        repo.done = True
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'enabled': False,
            'type': False,
            'name': False,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_repository_read_only(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config.repository
        control_agent = DetailRepositoryControlAgent(repo, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'enabled': False,
            'name':  False,
            'type':  False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_repository_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config.repository
        control_agent = DetailRepositoryControlAgent(repo, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        repo.enabled = True
        refresh_gui()

        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(presentation_agent.get_validity_flag(),
                        'site validity should be true')

        presentation_agent['name'].set_text('ab c')
        refresh_gui()
        self.assertFalse(presentation_agent.get_validity_flag(),
                        'site validity should be false')


class TestDetailDNSHostGtkPresentationAgent(BaseTestGtkPresentationAgent):
    """Unit tests for dnshost detail gtk presentation_agents"""

    def test_detail_dnshost_init_state(self):
        """
        Tests repository detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        dnshost = config.dnshost
        control_agent = DetailDNSHostControlAgent(dnshost)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests widgets sensitivity
        flags = {
            'description': not dnshost.done,
            'name': not dnshost.done,
            'domain': not dnshost.done,
            'platform': not dnshost.done,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_dnshost_done_state(self):
        """
        Tests dnshost detail component's presentation agent in done state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        dnshost = config.dnshost
        dnshost.done = True
        control_agent = DetailDNSHostControlAgent(dnshost)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests widgets sensitivity
        flags = {
            'description': not dnshost.done,
            'name': not dnshost.done,
            'domain': not dnshost.done,
            'platform': not dnshost.done,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_dnshost_gui_actions(self):
        """
        Tests that repository detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        dnshost = config.dnshost
        control_agent = DetailDNSHostControlAgent(dnshost)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # When name entry is set, the abstraction should have corresponding
        # value set
        for name in ('name', 'description'):
            presentation_agent[name].set_text('abc')
            refresh_gui()
            self.assertEquals(getattr(dnshost, name), 'abc',
                              'dnshost %s attribute is wrong: %s' % (name, getattr(dnshost, name)))

        # Comboboxes value should be reported to abstraction
        domain = SiteDefaultsManager.get_domains().keys()[0]
        platform = SiteDefaultsManager.get_platforms().keys()[0]

        for name, value in {'domain': domain, 'platform': platform}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(getattr(dnshost, name), value,
                             'dnshost %s attribute is wrong' % name)

    def test_detail_dnshost_abstraction_actions(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        dnshost = config.dnshost
        control_agent = DetailDNSHostControlAgent(dnshost)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # All widgets should be enabled
        flags = {
            'name': True,
            'domain': True,
            'platform': True,
            'description': True
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # When a name or description is set, correpsonding widget
        # should follow
        for name in ('name', 'description'):
            setattr(dnshost, name, 'abc')
            refresh_gui()
            self.assertEquals(presentation_agent[name].get_text(), 'abc',
                             'dnshost %s widget is wrong' % name)

        # Comboboxes value should reflect abstraction changes
        domain = SiteDefaultsManager.get_domains().keys()[0]
        platform = SiteDefaultsManager.get_platforms().keys()[0]

        for name, value in {'domain': domain, 'platform': platform}.items():
            setattr(dnshost, name, value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'dnshost %s widget selection is wrong' % name)

        # Tests that when done flag is set, allw widgets are disabled
        dnshost.done = True
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'description': False,
            'name': False,
            'domain': False,
            'platform': False,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_dnshost_read_only(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        dnshost = config.dnshost
        control_agent = DetailDNSHostControlAgent(dnshost, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'name': False,
            'domain': False,
            'platform': False,
            'description': False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_dnshost_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        dnshost = config.dnshost
        control_agent = DetailDNSHostControlAgent(dnshost)
        presentation_agent = control_agent.get_presentation_agent()

        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(presentation_agent.get_validity_flag(),
                        'site validity should be true')

        presentation_agent['name'].set_text('@bc')
        refresh_gui()
        self.assertFalse(presentation_agent.get_validity_flag(),
                        'dnshost validity should be false')


if __name__ == "__main__":
    unittest.main()
