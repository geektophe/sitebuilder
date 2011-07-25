#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.controller.detail import DetailSiteController
from sitebuilder.controller.detail import DetailDatabaseController
from sitebuilder.controller.detail import DetailRepositoryController
from sitebuilder.controller.detail import DetailGeneralController

def get_default_site_controller():
    """
    Returns a DetailSiteController loaded with the default configuration
    """


class BaseTestGtkView(unittest.TestCase):
    """Unit test base class to be subclassed by real test cases"""

    def assert_widgets_active_flag(self, view, flags):
        """
        Checks that widgets active flag is set as of values dctionnary
        configuraiton.
        """
        for name, flag in flags.items():
            self.assertEquals(view[name].get_active(), flag,
                    "%s widget active flag sould be %s" % (name, flag))

    def assert_widgets_sensitive_flag(self, view, flags):
        """
        Checks that widgets active flag is set as of values dctionnary
        configuraiton.
        """

        for name, flag in flags.items():
            self.assertEquals(view[name].get_sensitive(), flag,
                    "%s widget sensitive flag sould be %s" % (name, flag))


class TestDetailSiteGtkView(BaseTestGtkView):
    """Unit tests for site detail gtk views"""

    def test_detail_site_init_state(self):
        """
        Tests site detail component's view initial state
        """
        config = ConfigurationManager.get_test_configuration(1)
        prod = config['sites']['prod']
        controller = DetailSiteController(prod)
        view = controller.get_view()
        refresh_gui()

        # Tests checkboxes state
        flags = {
            'enabled': prod['enabled'].get_value(),
            'proxied': prod['proxied'].get_value(),
            'maintenance': prod['maintenance'].get_value(),
            'name_def': prod['name'].get_value() == '__DEFAULT__',
            'name_cus': prod['name'].get_value() != '__DEFAULT__',
            }
        self.assert_widgets_active_flag(view, flags)

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
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_site_gui_actions(self):
        """
        Tests that site detail component's view works as expected, and that
        model attributes are set correspondingly to GUI actions.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        controller = DetailSiteController(prod)
        view = controller.get_view()
        view['enabled'].set_active(True)
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
        self.assert_widgets_sensitive_flag(view, flags)

        # Enabled attribute should be set to True in configuraiton
        self.assertTrue(prod['enabled'].get_value(),
                        'site configuraiton is not enabled')

        # When a widget is enabled, the corresponding attribute should follow
        for name in ('proxied', 'maintenance'):
            view[name].set_active(True)
            refresh_gui()
            self.assertTrue(prod[name].get_value(),
                            'site %s attribute is not enabled' % name)

        # When custom name radio button is pressed, name input should activate
        view['name_cus'].set_active(True)
        refresh_gui()
        self.assert_widgets_active_flag(view, {'name_def': False})
        self.assert_widgets_sensitive_flag(view, {'name': True})

        view['name'].set_text('abc')
        refresh_gui()
        self.assertEquals(prod['name'].get_value(), 'abc',
                        'site name attribute is wrong')

        # When custom name radio button is pressed, name input should disable
        view['name_def'].set_active(True)
        refresh_gui()
        self.assert_widgets_active_flag(view, {'name_cus': False})
        self.assert_widgets_sensitive_flag(view, {'name': False})

        self.assertEquals(prod['name'].get_value(), '__DEFAULT__',
                        'site name attribute is wrong')

        # Comboboxes value should be reported to model
        template = ConfigurationManager.get_site_templates().keys()[0]
        domain = ConfigurationManager.get_site_domains().keys()[0]

        for name, value in (('template', template), ('domain', domain)):
            view.set_combobox_selection(view[name], value)
            refresh_gui()

            self.assertEquals(prod[name].get_value(), value,
                            'site %s attribute is wrong' % name)

    def test_detail_site_model_actions(self):
        """
        Tests that site detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        controller = DetailSiteController(prod)
        view = controller.get_view()
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
        self.assert_widgets_sensitive_flag(view, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(view, {'enabled': True})

        # When a widget is enabled, the corresponding attribute should follow
        for name in ('proxied', 'maintenance'):
            prod[name].set_value(True)
            refresh_gui()
            self.assert_widgets_active_flag(view, {name: True})

        # When custom name is set, name_cus and name widgets should activate
        prod['name'].set_value('abc')
        refresh_gui()
        self.assert_widgets_active_flag(view, {'name_cus': True})
        self.assert_widgets_active_flag(view, {'name_def': False})
        self.assert_widgets_sensitive_flag(view, {'name': True})
        self.assertEquals(view['name'].get_text(), 'abc',
                         'site name widget text is wrong')

        # When custom name radio button is pressed, name input should disable
        prod['name'].set_value('__DEFAULT__')
        refresh_gui()
        self.assert_widgets_active_flag(view, {'name_cus': False})
        self.assert_widgets_active_flag(view, {'name_def': True})
        self.assert_widgets_sensitive_flag(view, {'name': False})

        # Comboboxes value should reflect model changes
        template = ConfigurationManager.get_site_templates().keys()[0]
        domain = ConfigurationManager.get_site_domains().keys()[0]

        for name, value in {'template': template, 'domain': domain}.items():
            prod[name].set_value(value)
            refresh_gui()
            self.assertEquals(view.get_combobox_selection(view[name]),
                    value, 'site %s widget selection is wrong' % name)

    def test_detail_site_read_only(self):
        """
        Tests that site detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        controller = DetailSiteController(prod, read_only=True)
        view = controller.get_view()
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
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_site_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['sites']['prod']
        controller = DetailSiteController(prod, read_only=True)
        view = controller.get_view()
        prod['enabled'].set_value(True)
        refresh_gui()

        view['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(view.get_validity_flag(),
                        'site validity should be true')

        view['name'].set_text('ab c')
        refresh_gui()
        self.assertFalse(view.get_validity_flag(),
                        'dite validity should be false')


class TestDetailDatabaseGtkView(BaseTestGtkView):
    """Unit tests for database detail gtk views"""

    def test_detail_database_init_state(self):
        """
        Tests site detail component's view initial state
        """
        config = ConfigurationManager.get_test_configuration(1)
        prod = config['databases']['prod']
        controller = DetailDatabaseController(prod)
        view = controller.get_view()
        refresh_gui()

        # Tests checkboxes state
        flags = { 'enabled': prod['enabled'].get_value() }
        self.assert_widgets_active_flag(view, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not prod['done'].get_value(),
            'name': prod['enabled'].get_value(),
            'username': prod['enabled'].get_value(),
            'password': prod['enabled'].get_value(),
            'type': prod['enabled'].get_value(),
            }
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_database_gui_actions(self):
        """
        Tests that database detail component's view works as expected, and that
        model attributes are set correspondingly to GUI actions.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['databases']['prod']
        controller = DetailDatabaseController(prod)
        view = controller.get_view()
        view['enabled'].set_active(True)
        refresh_gui()

        # All widgets should be enabled
        flags = { 'enabled': not prod['done'].get_value() }
        self.assert_widgets_sensitive_flag(view, flags)

        # Enabled attribute should be set to True in configuraiton
        self.assertTrue(prod['enabled'].get_value(),
                        'database configuraiton is not enabled')

        # When an entry is set, the model should have corresponding value set
        for name in ('name', 'username', 'password'):
            view[name].set_text('abc')
            refresh_gui()
            self.assertEquals(prod[name].get_value(), 'abc',
                             'database %s attribute is wrong' % name)

        # Comboboxes value should be reported to model
        dbtype = ConfigurationManager.get_database_types().keys()[0]

        view.set_combobox_selection(view['type'], dbtype)
        refresh_gui()
        self.assertEquals(prod['type'].get_value(), dbtype,
                         'database type attribute is wrong')

    def test_detail_database_model_actions(self):
        """
        Tests that database detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['databases']['prod']
        controller = DetailDatabaseController(prod)
        view = controller.get_view()
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
        self.assert_widgets_sensitive_flag(view, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(view, {'enabled': True})

        # When a name, username or password is set, correpsonding widget
        # should follow
        for name in ('name', 'username', 'password'):
            prod[name].set_value('abc')
            refresh_gui()
            self.assertEquals(view[name].get_text(), 'abc',
                             'database %s widget is wrong' % name)

        # Comboboxes value should reflect model changes
        dbtype = ConfigurationManager.get_database_types().keys()[0]

        prod['type'].set_value(dbtype)
        refresh_gui()
        self.assertEquals(view.get_combobox_selection(view['type']),
                dbtype, 'site type widget selection is wrong')

    def test_detail_database_read_only(self):
        """
        Tests that database detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['databases']['prod']
        controller = DetailDatabaseController(prod, read_only=True)
        view = controller.get_view()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'enabled': False,
            'name':  False,
            'username':  False,
            'password':  False,
            'type':  False
            }
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_database_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['databases']['prod']
        controller = DetailDatabaseController(prod, read_only=True)
        view = controller.get_view()
        prod['enabled'].set_value(True)
        refresh_gui()

        for widget in ('name', 'username'):
            view[widget].set_text('abc')
            refresh_gui()
            self.assertTrue(view.get_validity_flag(),
                            'database validity should be true')

            view[widget].set_text('ab c')
            refresh_gui()
            self.assertFalse(view.get_validity_flag(),
                            'database validity should be false')


class TestDetailRepositoryGtkView(BaseTestGtkView):
    """Unit tests for repository detail gtk views"""

    def test_detail_repository_init_state(self):
        """
        Tests repository detail component's view initial state
        """
        config = ConfigurationManager.get_test_configuration(1)
        repo = config['repository']
        controller = DetailRepositoryController(repo)
        view = controller.get_view()
        refresh_gui()

        # Tests checkboxes state
        flags = { 'enabled': repo['enabled'].get_value() }
        self.assert_widgets_active_flag(view, flags)

        # Tests widgets sensitivity
        flags = {
            'enabled': not repo['done'].get_value(),
            'name': repo['enabled'].get_value(),
            'type': repo['enabled'].get_value(),
            }
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_repository_gui_actions(self):
        """
        Tests that repository detail component's view works as expected, and
        that model attributes are set correspondingly to GUI actions.
        """
        config = ConfigurationManager.get_blank_configuration()
        repo = config['repository']
        controller = DetailRepositoryController(repo)
        view = controller.get_view()
        view['enabled'].set_active(True)
        refresh_gui()

        # All widgets should be enabled
        flags = { 'enabled': not repo['done'].get_value() }
        self.assert_widgets_sensitive_flag(view, flags)

        # Enabled attribute should be set to True in configuraiton
        self.assertTrue(repo['enabled'].get_value(),
                        'repository configuraiton is not enabled')

        # When name entry is set, the model should have corresponding value set
        view['name'].set_text('abc')
        refresh_gui()
        self.assertEquals(repo['name'].get_value(), 'abc',
                             'repository name attribute is wrong')

        # Comboboxes value should be reported to model
        repotype = ConfigurationManager.get_repository_types().keys()[0]

        view.set_combobox_selection(view['type'], repotype)
        refresh_gui()
        self.assertEquals(repo['type'].get_value(), repotype,
                         'repository type attribute is wrong')

    def test_detail_repository_model_actions(self):
        """
        Tests that database detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        repo = config['repository']
        controller = DetailRepositoryController(repo)
        view = controller.get_view()
        repo['enabled'].set_value(True)
        refresh_gui()

        # All widgets should be enabled
        flags = {
            'enabled': not repo['done'].get_value(),
            'name': repo['enabled'].get_value(),
            'type': repo['enabled'].get_value(),
            }
        self.assert_widgets_sensitive_flag(view, flags)

        # Enabled widget should be activated
        self.assert_widgets_active_flag(view, {'enabled': True})

        # When name is set, correpsonding widget should follow
        repo['name'].set_value('abc')
        refresh_gui()
        self.assertEquals(view['name'].get_text(), 'abc',
                         'repository name widget is wrong')

        # Comboboxes value should reflect model changes
        repotype = ConfigurationManager.get_repository_types().keys()[0]

        repo['type'].set_value(repotype)
        refresh_gui()
        self.assertEquals(view.get_combobox_selection(view['type']),
                repotype, 'site type widget selection is wrong')

    def test_detail_repository_read_only(self):
        """
        Tests that database detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        repo = config['repository']
        controller = DetailRepositoryController(repo, read_only=True)
        view = controller.get_view()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'enabled': False,
            'name':  False,
            'type':  False
            }
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_repository_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['repository']
        controller = DetailRepositoryController(prod, read_only=True)
        view = controller.get_view()
        prod['enabled'].set_value(True)
        refresh_gui()

        view['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(view.get_validity_flag(),
                        'site validity should be true')

        view['name'].set_text('ab c')
        refresh_gui()
        self.assertFalse(view.get_validity_flag(),
                        'dite validity should be false')


class TestDetailGeneralGtkView(BaseTestGtkView):
    """Unit tests for general detail gtk views"""

    def test_detail_general_init_state(self):
        """
        Tests repository detail component's view initial state
        """
        config = ConfigurationManager.get_test_configuration(1)
        general = config['general']
        controller = DetailGeneralController(general)
        view = controller.get_view()
        refresh_gui()

        # Tests widgets sensitivity
        flags = {
            'name': True,
            'description': True,
            }
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_general_gui_actions(self):
        """
        Tests that repository detail component's view works as expected, and
        that model attributes are set correspondingly to GUI actions.
        """
        config = ConfigurationManager.get_blank_configuration()
        general = config['general']
        controller = DetailGeneralController(general)
        view = controller.get_view()
        refresh_gui()

        # When name entry is set, the model should have corresponding value set
        view['name'].set_text('abc')
        refresh_gui()
        self.assertEquals(general['name'].get_value(), 'abc',
                             'general name attribute is wrong')

        view['description'].set_text('abc')
        refresh_gui()
        self.assertEquals(general['description'].get_value(), 'abc',
                             'general description attribute is wrong')

    def test_detail_general_model_actions(self):
        """
        Tests that database detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        general = config['general']
        controller = DetailGeneralController(general)
        view = controller.get_view()
        refresh_gui()

        # All widgets should be enabled
        flags = { 'name': True, 'description': True }
        self.assert_widgets_sensitive_flag(view, flags)

        # When name is set, correpsonding widget should follow
        general['name'].set_value('abc')
        refresh_gui()
        self.assertEquals(view['name'].get_text(), 'abc',
                         'general name widget is wrong')

        # When description is set, correpsonding widget should follow
        general['description'].set_value('abc')
        refresh_gui()
        self.assertEquals(view['name'].get_text(), 'abc',
                         'general description widget is wrong')

    def test_detail_general_read_only(self):
        """
        Tests that database detail component's models changes are correctly
        reported to GUI.
        """
        config = ConfigurationManager.get_blank_configuration()
        general = config['general']
        controller = DetailGeneralController(general, read_only=True)
        view = controller.get_view()
        refresh_gui()

        # Ine read-only mode, all widgets should be disabled
        flags = {
            'name':  False,
            'description':  False
            }
        self.assert_widgets_sensitive_flag(view, flags)

    def test_detail_general_validity_flag(self):
        """
        Tests that the validity flag is correctly set and unset when a
        component's widget value is set to a correct and incorrect value.
        """
        config = ConfigurationManager.get_blank_configuration()
        prod = config['general']
        controller = DetailGeneralController(prod, read_only=True)
        view = controller.get_view()

        view['name'].set_text('abc')
        refresh_gui()
        self.assertTrue(view.get_validity_flag(),
                        'site validity should be true')

        view['name'].set_text('@bc')
        refresh_gui()
        self.assertFalse(view.get_validity_flag(),
                        'dite validity should be false')


if __name__ == "__main__":
    unittest.main()
