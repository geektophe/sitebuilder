#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
from sitebuilder.utils.parameters import set_application_context
from sitebuilder.abstraction.site import SiteConfigurationManager
from sitebuilder.control.detail import DetailSiteControlAgent
from sitebuilder.control.detail import DetailDatabaseControlAgent
from sitebuilder.control.detail import DetailRepositoryControlAgent
from sitebuilder.control.detail import DetailGeneralControlAgent


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

    def detail_site_state_test(self, website):
        """
        Tests site detail component's presentation_agent initial state
        """
        control_agent = DetailSiteControlAgent(website)
        presentation_agent = control_agent.get_presentation_agent()
        done = website['done'].get_value()
        enabled = website['enabled'].get_value()
        refresh_gui()

        # Tests checkboxes state
        flags = {
            'enabled': website['enabled'].get_value(),
            'maintenance': website['maintenance'].get_value(),
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

    def test_detail_site_init_state(self):
        """
        Tests site detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config['website']
        self.detail_site_state_test(website)

    def test_detail_site_enabled_state(self):
        """
        Tests site detail component's presentation_agent in done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config['website']
        website['enabled'].set_value(True)
        self.detail_site_state_test(website)

    def test_detail_site_done_state(self):
        """
        Tests site detail component's presentation_agent in done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config['website']
        website['enabled'].set_value(True)
        website['done'].set_value(True)
        self.detail_site_state_test(website)

    def test_detail_site_gui_actions(self):
        """
        Tests that site detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config['website']
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
            self.assertTrue(website[name].get_value(),
                            'site %s attribute is not enabled' % name)

        # Comboboxes value should be reported to abstraction
        template = SiteConfigurationManager.get_site_templates().keys()[0]
        access = SiteConfigurationManager.get_site_accesses().keys()[0]

        for name, value in {'template': template, 'access': access}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(website[name].get_value(), value,
                             'site %s attribute is wrong' % name)

    def test_detail_site_abstraction_actions(self):
        """
        Tests that site detail component's abstractions changes are correctly
        reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config['website']
        control_agent = DetailSiteControlAgent(website)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Enables component
        website['enabled'].set_value(True)
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
            website[name].set_value(True)
            refresh_gui()
            self.assert_widgets_active_flag(presentation_agent, {name: True})

        # Comboboxes value should reflect abstraction changes
        template = SiteConfigurationManager.get_site_templates().keys()[0]
        access = SiteConfigurationManager.get_site_accesses().keys()[0]

        for name, value in {'template': template, 'access': access}.items():
            website[name].set_value(value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'site %s widget selection is wrong' % name)

        # Tests that when done flag is set, sentivity is disabled on enabled
        # and template widgets. Maintenance and access should remain sensitive
        website['done'].set_value(True)
        refresh_gui()

        # Tests final widgets sensitivity
        flags = {
            'enabled': False,
            'template': False,
            'maintenance': True,
            'access': True,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_site_read_only(self):
        """
        Tests that site detail component's abstractions changes are correctly
        reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        website = config['website']
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
        done = database['done'].get_value()
        enabled = database['enabled'].get_value()
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
        database = config['database']
        self.detail_database_state_test(database)

    def test_detail_database_enabled_state(self):
        """
        Tests site detail component's presentation_agent n done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config['database']
        database['enabled'].set_value(True)
        self.detail_database_state_test(database)

    def test_detail_database_done_state(self):
        """
        Tests site detail component's presentation_agent n done state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config['database']
        database['enabled'].set_value(True)
        database['done'].set_value(True)
        self.detail_database_state_test(database)

    def test_detail_database_gui_actions(self):
        """
        Tests that database detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config['database']
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
            database[name].set_value(True)
            refresh_gui()
            self.assert_widgets_active_flag(presentation_agent, {name: True})

        # When an entry is set, the abstraction should have corresponding
        # value set
        for name in ('name', 'username', 'password'):
            presentation_agent[name].set_text('abc')
            refresh_gui()
            self.assertEquals(database[name].get_value(), 'abc',
                             'database %s attribute is wrong' % name)

        # Comboboxes value should be reported to abstraction
        dbtype = SiteConfigurationManager.get_database_types().keys()[0]

        for name, value in {'type': dbtype}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(database[name].get_value(), value,
                             'site %s attribute is wrong' % name)

    def test_detail_database_abstraction_actions(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        database = config['database']
        control_agent = DetailDatabaseControlAgent(database)
        presentation_agent = control_agent.get_presentation_agent()
        database['enabled'].set_value(True)
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
            database[name].set_value('abc')
            refresh_gui()
            self.assertEquals(presentation_agent[name].get_text(), 'abc',
                             'database %s widget is wrong' % name)

        # Comboboxes value should reflect abstraction changes
        dbtype = SiteConfigurationManager.get_database_types().keys()[0]

        for name, value in {'type': dbtype}.items():
            database[name].set_value(value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'database %s widget selection is wrong' % name)

        # Tests that when done flag is set, allw widgets are disabled
        database['done'].set_value(True)
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
        database = config['database']
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
        database = config['database']
        control_agent = DetailDatabaseControlAgent(database, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        database['enabled'].set_value(True)
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
        done = repo['done'].get_value()
        enabled = repo['enabled'].get_value()
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
        repo = config['repository']
        self.detail_repository_state_test(repo)

    def test_detail_repository_enabled_state(self):
        """
        Tests repo detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config['repository']
        repo['enabled'].set_value(True)
        self.detail_repository_state_test(repo)

    def test_detail_repository_done_state(self):
        """
        Tests repo detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config['repository']
        repo['enabled'].set_value(True)
        repo['done'].set_value(True)
        self.detail_repository_state_test(repo)

    def test_detail_repository_gui_actions(self):
        """
        Tests that repo detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config['repository']
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
            self.assertTrue(repo[name].get_value(),
                            'repo %s attribute is not enabled' % name)

        # Comboboxes value should be reported to abstraction
        repotype = SiteConfigurationManager.get_repository_types().keys()[0]

        for name, value in {'type': repotype}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(repo[name].get_value(), value,
                             'repo %s attribute is wrong' % name)

    def test_detail_repository_abstraction_actions(self):
        """
        Tests that repo detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config['repository']
        control_agent = DetailRepositoryControlAgent(repo)
        presentation_agent = control_agent.get_presentation_agent()
        repo['enabled'].set_value(True)
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
            repo[name].set_value('abc')
            refresh_gui()
            self.assertEquals(presentation_agent[name].get_text(), 'abc',
                             'repo %s widget is wrong' % name)

        # Comboboxes value should reflect abstraction changes
        repotype = SiteConfigurationManager.get_repository_types().keys()[0]

        for name, value in {'type': repotype}.items():
            repo[name].set_value(value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'repo %s widget selection is wrong' % name)

        # Tests that when done flag is set, allw widgets are disabled
        repo['done'].set_value(True)
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
        repo = config['repository']
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
        prod = config['repository']
        control_agent = DetailRepositoryControlAgent(prod, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        prod['enabled'].set_value(True)
        refresh_gui()

        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(presentation_agent.get_validity_flag(),
                        'site validity should be true')

        presentation_agent['name'].set_text('ab c')
        refresh_gui()
        self.assertFalse(presentation_agent.get_validity_flag(),
                        'dite validity should be false')


class TestDetailGeneralGtkPresentationAgent(BaseTestGtkPresentationAgent):
    """Unit tests for general detail gtk presentation_agents"""

    def test_detail_general_init_state(self):
        """
        Tests repository detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        general = config['general']
        control_agent = DetailGeneralControlAgent(general)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests widgets sensitivity
        flags = {
            'description': not general['done'].get_value(),
            'name': not general['done'].get_value(),
            'domain': not general['done'].get_value(),
            'platform': not general['done'].get_value(),
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_general_done_state(self):
        """
        Tests general detail component's presentation agent in done state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        general = config['general']
        general['done'].set_value(True)
        control_agent = DetailGeneralControlAgent(general)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests widgets sensitivity
        flags = {
            'description': not general['done'].get_value(),
            'name': not general['done'].get_value(),
            'domain': not general['done'].get_value(),
            'platform': not general['done'].get_value(),
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_general_gui_actions(self):
        """
        Tests that repository detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        general = config['general']
        control_agent = DetailGeneralControlAgent(general)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # When name entry is set, the abstraction should have corresponding
        # value set
        for name in ('name', 'description'):
            presentation_agent[name].set_text('abc')
            refresh_gui()
            self.assertEquals(general[name].get_value(), 'abc',
                             'general %s attribute is wrong' % name)

        # Comboboxes value should be reported to abstraction
        domain = SiteConfigurationManager.get_domains().keys()[0]
        platform = SiteConfigurationManager.get_platforms().keys()[0]

        for name, value in {'domain': domain, 'platform': platform}.items():
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()
            self.assertEquals(general[name].get_value(), value,
                             'general %s attribute is wrong' % name)

    def test_detail_general_abstraction_actions(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        general = config['general']
        control_agent = DetailGeneralControlAgent(general)
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
            general[name].set_value('abc')
            refresh_gui()
            self.assertEquals(presentation_agent[name].get_text(), 'abc',
                             'general %s widget is wrong' % name)

        # Comboboxes value should reflect abstraction changes
        domain = SiteConfigurationManager.get_domains().keys()[0]
        platform = SiteConfigurationManager.get_platforms().keys()[0]

        for name, value in {'domain': domain, 'platform': platform}.items():
            general[name].set_value(value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'general %s widget selection is wrong' % name)

        # Tests that when done flag is set, allw widgets are disabled
        general['done'].set_value(True)
        refresh_gui()

        # Tests widgets sensitivity after enablement
        flags = {
            'description': False,
            'name': False,
            'domain': False,
            'platform': False,
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_general_read_only(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        general = config['general']
        control_agent = DetailGeneralControlAgent(general, read_only=True)
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

    def test_detail_general_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        general = config['general']
        control_agent = DetailGeneralControlAgent(general, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()

        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(presentation_agent.get_validity_flag(),
                        'site validity should be true')

        presentation_agent['name'].set_text('@bc')
        refresh_gui()
        self.assertFalse(presentation_agent.get_validity_flag(),
                        'general validity should be false')


if __name__ == "__main__":
    unittest.main()
