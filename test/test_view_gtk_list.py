#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
from sitebuilder.utils.parameters import set_application_context
from sitebuilder.controller.list import ListController
from sitebuilder.model.configuration import ConfigurationManager


class ListTestController(ListController):
    """
    List test controller used to test view behaviour
    """

    def __init__(self):
        """
        Initializes controller.
        """
        ListController.__init__(self)
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
        Returns data that should have been passed to detail main controller
        """
        return self._detail_dialog_data

    def get_delete_configuration_data(self):
        """
        Returns data that should have been passed to detail main controller
        """
        return self._detail_delete_id


class TestGtkListView(unittest.TestCase):
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
        controller = ListTestController()
        view = controller.get_view()
        model = view['site_list'].get_model()

        configurations = ConfigurationManager.get_configuration_all()
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
        Tests that the correct parameters are sent by controller when add
        action is activated.
        """
        controller = ListTestController()
        view = controller.get_view()
        view['add'].activate()
        refresh_gui()
        configuration, read_only = controller.get_detail_configuration_data()
        confid = configuration['general']['id'].get_value()
        self.assertFalse(read_only)
        self.assertTrue(confid is None)

    def test_list_view_action(self):
        """
        Tests that the correct parameters are sent by controller when add
        action is activated.
        """

        row = 0
        controller = ListTestController()
        view = controller.get_view()
        view['site_list'].get_selection().select_path((row,))
        view['view'].activate()
        refresh_gui()
        configuration, read_only = controller.get_detail_configuration_data()
        confid = configuration['general']['id'].get_value()

        testconf = ConfigurationManager.get_configuration_all()[row]
        testid = testconf['general']['id'].get_value()

        self.assertEquals(confid, testid)
        self.assertTrue(read_only)

    def test_list_edit_action(self):
        """
        Tests that the correct parameters are sent by controller when add
        action is activated.
        """

        row = 0
        controller = ListTestController()
        view = controller.get_view()
        view['site_list'].get_selection().select_path((row,))
        view['edit'].activate()
        refresh_gui()
        configuration, read_only = controller.get_detail_configuration_data()
        confid = configuration['general']['id'].get_value()

        testconf = ConfigurationManager.get_configuration_all()[row]
        testid = testconf['general']['id'].get_value()

        self.assertEquals(confid, testid)
        self.assertFalse(read_only)


if __name__ == "__main__":
    unittest.main()
