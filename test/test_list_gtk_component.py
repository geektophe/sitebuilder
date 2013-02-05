#!/usr/bin/env python
"""
Test classes for view.gtk.detail views classes
"""

import unittest
from gtktest import refresh_gui
#from sitebuilder.utils.parameters import set_application_context
#from sitebuilder.control.list import ListSitesControlAgent
from sitebuilder.control.list import ListLogsControlAgent
#from sitebuilder.abstraction.site.manager import SiteConfigurationManager
from sitebuilder.command.base import BaseCommand
from sitebuilder.observer.command import ICommandSubject, CommandSubject
from sitebuilder.command.interface import COMMAND_SUCCESS
from sitebuilder.application import init, uninit
from zope.interface import implements


class TestCommand(BaseCommand, CommandSubject):
    """
    Test action that does nothing
    """
    implements(ICommandSubject)

    description = "Dummy test command"

    def __init__(self):
        """
        Command initialization
        """
        BaseCommand.__init__(self)
        CommandSubject.__init__(self)

    def execute(self, driver):
        """
        Null method that does nothing
        """


#class ListSitesTestControlAgent(ListSitesControlAgent):
#    """
#    List test control agent used to test presentation_agent behaviour
#    """
#
#    def __init__(self):
#        """
#        Initializes control agent.
#        """
#        ListSitesControlAgent.__init__(self)
#        self._detail_dialog_data = ()
#        self._detail_delete_id = None
#
#    def show_detail_dialog(self, site, read_only=False):
#        """
#        Shows detail dialog for the specified site
#        """
#        self._detail_dialog_data = (site, read_only)
#
#    def show_delete_dialog(self, confid):
#        """
#        Shows detail dialog for the specified site
#        """
#        self._detail_delete_id = confid
#
#    def get_detail_site_data(self):
#        """
#        Returns data that should have been passed to detail main control agent
#        """
#        return self._detail_dialog_data
#
#    def get_delete_site_data(self):
#        """
#        Returns data that should have been passed to detail main control agent
#        """
#        return self._detail_delete_id
#
#
#class TestGtkListSitesPresentationAgent(unittest.TestCase):
#    """Unit test base class to be subclassed by real test cases"""
#
#    def setUp(self):
#        """
#        Enables test context
#        """
#        init()
#        set_application_context('test')
#
#    def tearDown(self):
#        """
#        Cleans execution context
#        """
#        uninit()
#        sleep(0.5)
#
#    def test_list_site_content(self):
#        """
#        Tests that test site is correctly loaded into interface's
#        treeview component
#        """
#        control_agent = ListSitesTestControlAgent()
#        presentation_agent = control_agent.get_presentation_agent()
#        model = presentation_agent['site_list'].get_model()
#
#        hosts = SiteConfigurationManager.lookup_host_by_name("*", "*")
#        self.assertEquals(len(hosts), len(model))
#
#        for i in range(len(hosts)):
#            dnshost = hosts[i]
#            row = model[i]
#
#            conf_name = dnshost.name
#            conf_domain = dnshost.domain
#            conf_plat = dnshost.platform
#            conf_desc = dnshost.description
#
#            row_name = row[0]
#            row_domain = row[1]
#            row_plat = row[2]
#            row_desc = row[3]
#
#            self.assertEquals(conf_name, row_name)
#            self.assertEquals(conf_domain, row_domain)
#            self.assertEquals(conf_plat, row_plat)
#            self.assertEquals(conf_desc, row_desc)
#
#    def test_list_add_action(self):
#        """
#        Tests that the correct parameters are sent by control agent when add
#        action is activated.
#        """
#        control_agent = ListSitesTestControlAgent()
#        presentation_agent = control_agent.get_presentation_agent()
#        presentation_agent['add'].activate()
#        refresh_gui()
#        site, read_only = control_agent.get_detail_site_data()
#        self.assertFalse(read_only)
#
#    def test_list_view_action(self):
#        """
#        Tests that the correct parameters are sent by control agent when add
#        action is activated.
#        """
#        row = 0
#        control_agent = ListSitesTestControlAgent()
#        presentation_agent = control_agent.get_presentation_agent()
#        presentation_agent['site_list'].get_selection().select_path((row,))
#        presentation_agent['view'].activate()
#        refresh_gui()
#        site, read_only = control_agent.get_detail_site_data()
#
#        conf_fqdn = "%s.%s" % (
#            site.dnshost.name,
#            site.dnshost.domain)
#
#        testconf = SiteConfigurationManager.lookup_host_by_name("*", "*")[row]
#
#        test_fqdn = "%s.%s" % (
#            testconf.name,
#            testconf.domain)
#
#        self.assertEquals(conf_fqdn, test_fqdn)
#        self.assertTrue(read_only)
#
#    def test_list_edit_action(self):
#        """
#        Tests that the correct parameters are sent by control agent when add
#        action is activated.
#        """
#        row = 0
#        control_agent = ListSitesTestControlAgent()
#        presentation_agent = control_agent.get_presentation_agent()
#        presentation_agent['site_list'].get_selection().select_path((row,))
#        presentation_agent['edit'].activate()
#        refresh_gui()
#        site, read_only = control_agent.get_detail_site_data()
#
#        conf_fqdn = "%s.%s" % (
#            site.dnshost.name,
#            site.dnshost.domain)
#
#        testconf = SiteConfigurationManager.lookup_host_by_name("*", "*")[row]
#
#        test_fqdn = "%s.%s" % (
#            testconf.name,
#            testconf.domain)
#
#        self.assertEquals(conf_fqdn, test_fqdn)
#        self.assertFalse(read_only)


class TestGtkListLogsAgent(unittest.TestCase):
    """Unit test base class to be subclassed by real test cases"""

    def test_list_logs_content(self):
        """
        Tests that logs list initial content is empty
        """
        control_agent = ListLogsControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        model = presentation_agent['logs_list'].get_model()
        refresh_gui()
        self.assertEquals(len(model), 0)

    def test_list_logs_command_execution(self):
        """
        Tests that a command executed notification adds the command to logs
        list
        """
        control_agent = ListLogsControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        model = presentation_agent['logs_list'].get_model()
        command = TestCommand()
        command.add_callback(control_agent)
        command.notify_command_executed()
        refresh_gui()
        self.assertEquals(len(model), 1)
        modrow = model[0]
        self.assertTrue(modrow[3] is command)

    def test_list_logs_clear(self):
        """
        Tests that a command executed notification adds the command to logs
        list
        """
        control_agent = ListLogsControlAgent()
        presentation_agent = control_agent.get_presentation_agent()
        model = presentation_agent['logs_list'].get_model()
        command = TestCommand()
        command.register_command_observer(control_agent)
        command.notify_command_executed()
        presentation_agent['clearlogs'].activate()
        refresh_gui()
        self.assertEquals(len(model), 0)


if __name__ == "__main__":
    unittest.main()
