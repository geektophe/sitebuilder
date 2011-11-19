#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
from sitebuilder.utils.parameters import set_application_context
from sitebuilder.control.list import ListControlAgent
from sitebuilder.abstraction.site.manager import SiteConfigurationManager


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

    def show_detail_dialog(self, site, read_only=False):
        """
        Shows detail dialog for the specified site
        """
        self._detail_dialog_data = (site, read_only)

    def show_delete_dialog(self, confid):
        """
        Shows detail dialog for the specified site
        """
        self._detail_delete_id = confid

    def get_detail_site_data(self):
        """
        Returns data that should have been passed to detail main control agent
        """
        return self._detail_dialog_data

    def get_delete_site_data(self):
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

    def test_list_site_content(self):
        """
        Tests that test site is correctly loaded into interface's
        treeview component
        """
        control_agent = ListTestControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        model = presentation_agent['site_list'].get_model()

        sites = SiteConfigurationManager.lookup_site_by_name("*", "*")
        self.assertEquals(len(sites), len(model))

        for i in range(len(sites)):
            dnshost = sites[i]
            row = model[i]

            conf_name = dnshost.name
            conf_domain = dnshost.domain
            conf_plat = dnshost.platform
            conf_desc = dnshost.description

            row_name = row[0]
            row_domain = row[1]
            row_plat = row[2]
            row_desc = row[3]

            self.assertEquals(conf_name, row_name)
            self.assertEquals(conf_domain, row_domain)
            self.assertEquals(conf_plat, row_plat)
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
        site, read_only = control_agent.get_detail_site_data()
        self.assertFalse(read_only)

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
        site, read_only = control_agent.get_detail_site_data()

        conf_fqdn = "%s.%s" % (
            site.dnshost.name,
            site.dnshost.domain)

        testconf = SiteConfigurationManager.lookup_site_by_name("*", "*")[row]

        test_fqdn = "%s.%s" % (
            testconf.name,
            testconf.domain)

        self.assertEquals(conf_fqdn, test_fqdn)
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
        site, read_only = control_agent.get_detail_site_data()

        conf_fqdn = "%s.%s" % (
            site.dnshost.name,
            site.dnshost.domain)

        testconf = SiteConfigurationManager.lookup_site_by_name("*", "*")[row]

        test_fqdn = "%s.%s" % (
            testconf.dnshost.name,
            testconf.dnshost.domain)

        self.assertEquals(conf_fqdn, test_fqdn)
        self.assertFalse(read_only)


if __name__ == "__main__":
    unittest.main()
