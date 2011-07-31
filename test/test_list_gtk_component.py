#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
from sitebuilder.utils.parameters import set_application_context
from sitebuilder.control.list import ListControlAgent
from sitebuilder.abstraction.site import SiteConfigurationManager


class ListTestControlAgent(ListControlAgent):
    """
    List test control agent used to test presentation_agent behaviour
    """

    def __init__(self):
        """
        Initializes control agent.
        """
        ListControlAgent.__init__(self)
        self._detail_dialog_data = ()
        self._detail_delete_id = None

    def show_detail_dialog(self, configuration, read_only=False):
        """
        Shows detail dialog for the specified configuration
        """
        self._detail_dialog_data = (configuration, read_only)

    def show_delete_dialog(self, confid):
        """
        Shows detail dialog for the specified configuration
        """
        self._detail_delete_id = confid

    def get_detail_configuration_data(self):
        """
        Returns data that should have been passed to detail main control agent
        """
        return self._detail_dialog_data

    def get_delete_configuration_data(self):
        """
        Returns data that should have been passed to detail main control agent
        """
        return self._detail_delete_id


class TestGtkListPresentationAgent(unittest.TestCase):
    """Unit test base class to be subclassed by real test cases"""

    def setUp(self):
        """
        Enables test context
        """
        set_application_context('test')

    def test_list_configuration_content(self):
        """
        Tests that test configuration is correctly loaded into interface's
        treeview component
        """
        control_agent = ListTestControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        model = presentation_agent['site_list'].get_model()

        configurations = SiteConfigurationManager.get_configuration_all()
        self.assertEquals(len(configurations), len(model))

        for i in range(len(configurations)):
            configuration = configurations[i]
            row = model[i]

            conf_id = configuration['general']['id'].get_value()
            conf_name = configuration['general']['name'].get_value()
            conf_desc = configuration['general']['description'].get_value()

            row_id = int(row[0])
            row_name = row[1]
            row_desc = row[2]

            self.assertEquals(conf_id, row_id)
            self.assertEquals(conf_name, row_name)
            self.assertEquals(conf_desc, row_desc)

    def test_list_add_action(self):
        """
        Tests that the correct parameters are sent by control agent when add
        action is activated.
        """
        control_agent = ListTestControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        presentation_agent['add'].activate()
        refresh_gui()
        configuration, read_only = control_agent.get_detail_configuration_data()
        confid = configuration['general']['id'].get_value()
        self.assertFalse(read_only)
        self.assertTrue(confid is None)

    def test_list_view_action(self):
        """
        Tests that the correct parameters are sent by control agent when add
        action is activated.
        """

        row = 0
        control_agent = ListTestControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        presentation_agent['site_list'].get_selection().select_path((row,))
        presentation_agent['view'].activate()
        refresh_gui()
        configuration, read_only = control_agent.get_detail_configuration_data()
        confid = configuration['general']['id'].get_value()

        testconf = SiteConfigurationManager.get_configuration_all()[row]
        testid = testconf['general']['id'].get_value()

        self.assertEquals(confid, testid)
        self.assertTrue(read_only)

    def test_list_edit_action(self):
        """
        Tests that the correct parameters are sent by control agent when add
        action is activated.
        """

        row = 0
        control_agent = ListTestControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        presentation_agent['site_list'].get_selection().select_path((row,))
        presentation_agent['edit'].activate()
        refresh_gui()
        configuration, read_only = control_agent.get_detail_configuration_data()
        confid = configuration['general']['id'].get_value()

        testconf = SiteConfigurationManager.get_configuration_all()[row]
        testid = testconf['general']['id'].get_value()

        self.assertEquals(confid, testid)
        self.assertFalse(read_only)


if __name__ == "__main__":
    unittest.main()
