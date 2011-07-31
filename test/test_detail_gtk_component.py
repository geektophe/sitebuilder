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

    def test_detail_site_init_state(self):
        """
        Tests site detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        prod = config['sites']['prod']
        control_agent = DetailSiteControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests checkboxes state
        flags = {
            'enabled': prod['enabled'].get_value(),
            'proxied': prod['proxied'].get_value(),
            'maintenance': prod['maintenance'].get_value(),
            'name_def': prod['name'].get_value() == '__DEFAULT__',
            'name_cus': prod['name'].get_value() != '__DEFAULT__',
            }
        self.assert_widgets_active_flag(presentation_agent, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not prod['done'].get_value(),
            'proxied': prod['enabled'].get_value(),
            'maintenance': prod['enabled'].get_value(),
            'name_def': prod['enabled'].get_value(),
            'name_cus': prod['enabled'].get_value(),
            'domain': prod['enabled'].get_value(),
            'template': prod['enabled'].get_value()
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_site_done_state(self):
        """
        Tests site detail component's presentation_agent in done state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        prod = config['sites']['prod']
        prod['done'].set_value(True)
        control_agent = DetailSiteControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests widgets sensitivity (in done state, all should be inactive
        # except proxied and maintenance)
        flags = {
            'enabled': False,
            'proxied': prod['enabled'].get_value(),
            'maintenance': prod['enabled'].get_value(),
            'name_def': False,
            'name_cus': False,
            'domain': False,
            'template': False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_site_gui_actions(self):
        """
        Tests that site detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        control_agent = DetailSiteControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        presentation_agent['enabled'].set_active(True)
        refresh_gui()

        # All widgets should be enabled
        flags = {
            'enabled': not prod['done'].get_value(),
            'proxied': prod['enabled'].get_value(),
            'maintenance': prod['enabled'].get_value(),
            'name_def': prod['enabled'].get_value(),
            'name_cus': prod['enabled'].get_value(),
            'domain': prod['enabled'].get_value(),
            'template': prod['enabled'].get_value()
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled attribute should be set to True in configuraiton
        self.assertTrue(prod['enabled'].get_value(),
                        'site configuraiton is not enabled')

        # When a widget is enabled, the corresponding attribute should follow
        for name in ('proxied', 'maintenance'):
            presentation_agent[name].set_active(True)
            refresh_gui()
            self.assertTrue(prod[name].get_value(),
                            'site %s attribute is not enabled' % name)

        # When custom name radio button is pressed, name input should activate
        presentation_agent['name_cus'].set_active(True)
        refresh_gui()
        self.assert_widgets_active_flag(presentation_agent,
                                        {'name_def': False})
        self.assert_widgets_sensitive_flag(presentation_agent, {'name': True})

        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertEquals(prod['name'].get_value(), 'abc',
                        'site name attribute is wrong')

        # When custom name radio button is pressed, name input should disable
        presentation_agent['name_def'].set_active(True)
        refresh_gui()
        self.assert_widgets_active_flag(presentation_agent,
                                        {'name_cus': False})
        self.assert_widgets_sensitive_flag(presentation_agent, {'name': False})

        self.assertEquals(prod['name'].get_value(), '__DEFAULT__',
                        'site name attribute is wrong')

        # Comboboxes value should be reported to abstraction
        template = SiteConfigurationManager.get_site_templates().keys()[0]
        domain = SiteConfigurationManager.get_site_domains().keys()[0]

        for name, value in (('template', template), ('domain', domain)):
            presentation_agent.set_combobox_selection(presentation_agent[name],
                                                      value)
            refresh_gui()

            self.assertEquals(prod[name].get_value(), value,
                            'site %s attribute is wrong' % name)

    def test_detail_site_abstraction_actions(self):
        """
        Tests that site detail component's abstractions changes are correctly
        reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        control_agent = DetailSiteControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        prod['enabled'].set_value(True)
        refresh_gui()

        # All widgets should be enabled
        flags = {
            'enabled': not prod['done'].get_value(),
            'proxied': prod['enabled'].get_value(),
            'maintenance': prod['enabled'].get_value(),
            'name_def': prod['enabled'].get_value(),
            'name_cus': prod['enabled'].get_value(),
            'domain': prod['enabled'].get_value(),
            'template': prod['enabled'].get_value()
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(presentation_agent, {'enabled': True})

        # When a widget is enabled, the corresponding attribute should follow
        for name in ('proxied', 'maintenance'):
            prod[name].set_value(True)
            refresh_gui()
            self.assert_widgets_active_flag(presentation_agent, {name: True})

        # When custom name is set, name_cus and name widgets should activate
        prod['name'].set_value('abc')
        refresh_gui()
        self.assert_widgets_active_flag(presentation_agent, {'name_cus': True})
        self.assert_widgets_active_flag(presentation_agent,
                                        {'name_def': False})
        self.assert_widgets_sensitive_flag(presentation_agent, {'name': True})
        self.assertEquals(presentation_agent['name'].get_text(), 'abc',
                         'site name widget text is wrong')

        # When custom name radio button is pressed, name input should disable
        prod['name'].set_value('__DEFAULT__')
        refresh_gui()
        self.assert_widgets_active_flag(presentation_agent,
                                        {'name_cus': False})
        self.assert_widgets_active_flag(presentation_agent, {'name_def': True})
        self.assert_widgets_sensitive_flag(presentation_agent, {'name': False})

        # Comboboxes value should reflect abstraction changes
        template = SiteConfigurationManager.get_site_templates().keys()[0]
        domain = SiteConfigurationManager.get_site_domains().keys()[0]

        for name, value in {'template': template, 'domain': domain}.items():
            prod[name].set_value(value)
            refresh_gui()
            self.assertEquals(presentation_agent.get_combobox_selection(
                presentation_agent[name]), value,
                'site %s widget selection is wrong' % name)

    def test_detail_site_read_only(self):
        """
        Tests that site detail component's abstractions changes are correctly
        reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        control_agent = DetailSiteControlAgent(prod, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'enabled': False,
            'proxied': False,
            'maintenance': False,
            'name_def': False,
            'name_cus': False,
            'domain': False,
            'template': False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_site_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        control_agent = DetailSiteControlAgent(prod, read_only=True)
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


class TestDetailDatabaseGtkPresentationAgent(BaseTestGtkPresentationAgent):
    """Unit tests for database detail gtk presentation_agents"""

    def test_detail_database_init_state(self):
        """
        Tests site detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        prod = config['databases']['prod']
        control_agent = DetailDatabaseControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests checkboxes state
        flags = { 'enabled': prod['enabled'].get_value() }
        self.assert_widgets_active_flag(presentation_agent, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not prod['done'].get_value(),
            'name': prod['enabled'].get_value(),
            'username': prod['enabled'].get_value(),
            'password': prod['enabled'].get_value(),
            'type': prod['enabled'].get_value(),
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_database_done_state(self):
        """
        Tests site detail component's presentation_agent n done state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        prod = config['databases']['prod']
        prod['done'].set_value(True)
        control_agent = DetailDatabaseControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests widgets sensitivity
        flags = {
            'enabled': False,
            'name': False,
            'username': False,
            'password': False,
            'type': False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_database_gui_actions(self):
        """
        Tests that database detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['databases']['prod']
        control_agent = DetailDatabaseControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        presentation_agent['enabled'].set_active(True)
        refresh_gui()

        # All widgets should be enabled
        flags = { 'enabled': not prod['done'].get_value() }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled attribute should be set to True in configuraiton
        self.assertTrue(prod['enabled'].get_value(),
                        'database configuraiton is not enabled')

        # When an entry is set, the abstraction should have corresponding
        # value set
        for name in ('name', 'username', 'password'):
            presentation_agent[name].set_text('abc')
            refresh_gui()
            self.assertEquals(prod[name].get_value(), 'abc',
                             'database %s attribute is wrong' % name)

        # Comboboxes value should be reported to abstraction
        dbtype = SiteConfigurationManager.get_database_types().keys()[0]

        presentation_agent.set_combobox_selection(presentation_agent['type'],
                                                  dbtype)
        refresh_gui()
        self.assertEquals(prod['type'].get_value(), dbtype,
                         'database type attribute is wrong')

    def test_detail_database_abstraction_actions(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['databases']['prod']
        control_agent = DetailDatabaseControlAgent(prod)
        presentation_agent = control_agent.get_presentation_agent()
        prod['enabled'].set_value(True)
        refresh_gui()

        # All widgets should be enabled
        flags = {
            'enabled': not prod['done'].get_value(),
            'name': prod['enabled'].get_value(),
            'username': prod['enabled'].get_value(),
            'password': prod['enabled'].get_value(),
            'type': prod['enabled'].get_value(),
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(presentation_agent, {'enabled': True})

        # When a name, username or password is set, correpsonding widget
        # should follow
        for name in ('name', 'username', 'password'):
            prod[name].set_value('abc')
            refresh_gui()
            self.assertEquals(presentation_agent[name].get_text(), 'abc',
                             'database %s widget is wrong' % name)

        # Comboboxes value should reflect abstraction changes
        dbtype = SiteConfigurationManager.get_database_types().keys()[0]

        prod['type'].set_value(dbtype)
        refresh_gui()
        self.assertEquals(
                presentation_agent.get_combobox_selection(
                    presentation_agent['type']),
                dbtype, 'site type widget selection is wrong')

    def test_detail_database_read_only(self):
        """
        Tests that database detail component's abstractions changes are
        correctly reported to GUI.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['databases']['prod']
        control_agent = DetailDatabaseControlAgent(prod, read_only=True)
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
        prod = config['databases']['prod']
        control_agent = DetailDatabaseControlAgent(prod, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()
        prod['enabled'].set_value(True)
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

    def test_detail_repository_init_state(self):
        """
        Tests repository detail component's presentation_agent initial state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        repo = config['repository']
        control_agent = DetailRepositoryControlAgent(repo)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests checkboxes state
        flags = { 'enabled': repo['enabled'].get_value() }
        self.assert_widgets_active_flag(presentation_agent, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not repo['done'].get_value(),
            'name': repo['enabled'].get_value(),
            'type': repo['enabled'].get_value(),
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_repository_done_state(self):
        """
        Tests repository detail component's presentation_agent in done state
        """
        config = SiteConfigurationManager.get_configuration_by_id(1)
        repo = config['repository']
        repo['done'].set_value(True)
        control_agent = DetailRepositoryControlAgent(repo)
        presentation_agent = control_agent.get_presentation_agent()
        refresh_gui()

        # Tests widgets sensitivity (in done state, all should be inactive)
        flags = {
            'enabled': False,
            'name': False,
            'type': False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_repository_gui_actions(self):
        """
        Tests that repository detail component's presentation_agent works as
        expected, and that abstraction attributes are set correspondingly to
        GUI actions.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        repo = config['repository']
        control_agent = DetailRepositoryControlAgent(repo)
        presentation_agent = control_agent.get_presentation_agent()
        presentation_agent['enabled'].set_active(True)
        refresh_gui()

        # All widgets should be enabled
        flags = { 'enabled': not repo['done'].get_value() }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled attribute should be set to True in configuraiton
        self.assertTrue(repo['enabled'].get_value(),
                        'repository configuraiton is not enabled')

        # When name entry is set, the abstraction should have corresponding
        # value set
        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertEquals(repo['name'].get_value(), 'abc',
                             'repository name attribute is wrong')

        # Comboboxes value should be reported to abstraction
        repotype = SiteConfigurationManager.get_repository_types().keys()[0]

        presentation_agent.set_combobox_selection(presentation_agent['type'],
                                                  repotype)
        refresh_gui()
        self.assertEquals(repo['type'].get_value(), repotype,
                         'repository type attribute is wrong')

    def test_detail_repository_abstraction_actions(self):
        """
        Tests that database detail component's abstractions changes are
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
            'enabled': not repo['done'].get_value(),
            'name': repo['enabled'].get_value(),
            'type': repo['enabled'].get_value(),
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(presentation_agent, {'enabled': True})

        # When name is set, correpsonding widget should follow
        repo['name'].set_value('abc')
        refresh_gui()
        self.assertEquals(presentation_agent['name'].get_text(), 'abc',
                         'repository name widget is wrong')

        # Comboboxes value should reflect abstraction changes
        repotype = SiteConfigurationManager.get_repository_types().keys()[0]

        repo['type'].set_value(repotype)
        refresh_gui()
        self.assertEquals(
            presentation_agent.get_combobox_selection(
                presentation_agent['type']),
            repotype, 'site type widget selection is wrong')

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
            'name': True,
            'description': True,
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
        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertEquals(general['name'].get_value(), 'abc',
                             'general name attribute is wrong')

        presentation_agent['description'].set_text('abc')
        refresh_gui()
        self.assertEquals(general['description'].get_value(), 'abc',
                             'general description attribute is wrong')

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
        flags = { 'name': True, 'description': True }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

        # When name is set, correpsonding widget should follow
        general['name'].set_value('abc')
        refresh_gui()
        self.assertEquals(presentation_agent['name'].get_text(), 'abc',
                         'general name widget is wrong')

        # When description is set, correpsonding widget should follow
        general['description'].set_value('abc')
        refresh_gui()
        self.assertEquals(presentation_agent['name'].get_text(), 'abc',
                         'general description widget is wrong')

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
            'name':  False,
            'description':  False
            }
        self.assert_widgets_sensitive_flag(presentation_agent, flags)

    def test_detail_general_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = SiteConfigurationManager.get_blank_configuration()
        prod = config['general']
        control_agent = DetailGeneralControlAgent(prod, read_only=True)
        presentation_agent = control_agent.get_presentation_agent()

        presentation_agent['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(presentation_agent.get_validity_flag(),
                        'site validity should be true')

        presentation_agent['name'].set_text('@bc')
        refresh_gui()
        self.assertFalse(presentation_agent.get_validity_flag(),
                        'dite validity should be false')


if __name__ == "__main__":
    unittest.main()
