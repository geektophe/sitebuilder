#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.controller.detail import DetailSiteController
from sitebuilder.controller.detail import DetailDatabaseController

def get_default_site_controller():
    """
    Returns a DetailSiteController loaded with the default configuration
    """


class BaseTestGtkView(unittest.TestCase):
    """Unit tests for database detail gtk views"""

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


if __name__ == "__main__":
    unittest.main()
