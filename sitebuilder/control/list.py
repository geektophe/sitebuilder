#!/usr/bin/env python
"""
Main list interface control agent
"""

from sitebuilder.presentation.gtk.list import ListPresentationAgent
from sitebuilder.control.detail import DetailMainControlAgent
from sitebuilder.abstraction.site.manager import SiteConfigurationManager
from sitebuilder.interfaces.action  import IActionObserver
from sitebuilder.utils.parameters import ACTION_ADD, ACTION_VIEW
from sitebuilder.utils.parameters import ACTION_EDIT, ACTION_DELETE
from zope.interface import implements
import gtk


class ListControlAgent(object):
    """
    List main component control agent
    """
    implements(IActionObserver)

    def __init__(self):
        """
        Initializes control agent.
        """
        self._presentation_agent = ListPresentationAgent(self)
        self._presentation_agent.register_action_observer(self)

    def action_activated(self, action=None):
        """
        ActionActivatedObserver trigger mmethod local implementation
        """
        # Handles add action that do nat need any parameter
        if action.name == ACTION_ADD:
            self.add_site()
            return

        # Checks that ids parameter is correctly set in event parameters
        parms = action.parameters

        if not parms.has_key('sites'):
            raise AttributeError('sites parameter is not set in action parameters')

        # Handles view action
        if action.name == ACTION_VIEW:
            self.view_selected_sites(parms['sites'])
        elif action.name == ACTION_EDIT:
            self.edit_selected_sites(parms['sites'])
        elif action.name == ACTION_DELETE:
            self.delete_selected_sites(parms['sites'])
        else:
            raise NotImplementedError("Unhandled action %s triggered" % action)

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def lookup_host_by_name(self, name, domain):
        """
        Retrieves all the configuraiton items from the abstraction
        """
        return SiteConfigurationManager.lookup_host_by_name(name, domain)

    def show_detail_dialog(self, site, read_only=False):
        """
        Shows detail dialog for the specified site
        """
        detail = DetailMainControlAgent(site, read_only)
        presentation = detail.get_presentation_agent()
        presentation.show()

    def show_delete_dialog(self, site):
        """
        Shows detail dialog for the specified site
        """
        dnshost = site.dnshost
        conf_name = "%s.%s" % (dnshost.name, dnshost.domain)

        dialog = gtk.MessageDialog(
            self.get_presentation_agent().get_toplevel(),
            gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
            "Are you sure you want to delete configuraiton '%s' ?" % conf_name)

        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_YES:
            print "deleted site id %s" % conf_name

    def add_site(self):
        """
        Display detail dialog in add mode with a new site site
        """
        site = SiteConfigurationManager.get_blank_site()
        self.show_detail_dialog(site)

    def view_selected_sites(self, selection):
        """
        Display detail dialog in view mode for each selected site id
        """
        for name, domain in selection:
            site = SiteConfigurationManager.get_site_by_name(
                name, domain)
            self.show_detail_dialog(site, True)

    def edit_selected_sites(self, selection):
        """
        Display detail dialog in edit mode for each selected site id
        """
        for name, domain in selection:
            site = SiteConfigurationManager.get_site_by_name(
                name, domain)
            self.show_detail_dialog(site)

    def delete_selected_sites(self, selection):
        """
        Display delete dialog for each selected site id
        """
        for name, domain in selection:
            site = SiteConfigurationManager.get_site_by_name(
                name, domain)
            self.show_delete_dialog(site)

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Destroyes presentation
        self._presentation_agent.register_action_observer(self)
        self._presentation_agent.destroy()


if __name__ == '__main__':
    control = ListControlAgent()
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
