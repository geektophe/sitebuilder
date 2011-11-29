#!/usr/bin/env python
"""
Main list interface control agent
"""

from sitebuilder.presentation.gtk.list import ListPresentationAgent
from sitebuilder.control.detail import DetailMainControlAgent
from sitebuilder.abstraction.site.factory import site_factory
from sitebuilder.interfaces.action  import IActionObserver, IActionSubject
from sitebuilder.interfaces.command import ICommandObserver, COMMAND_SUCCESS
from sitebuilder.interfaces.site import ISiteNew
from sitebuilder.utils.parameters import ACTION_ADD, ACTION_VIEW, ACTION_SUBMIT
from sitebuilder.utils.parameters import ACTION_EDIT, ACTION_DELETE
from sitebuilder.command.scheduler import enqueue_command
from sitebuilder.command.host import LookupHostByName
from sitebuilder.command.site import GetSiteByName, AddSite, UpdateSite
from sitebuilder.command.site import DeleteSite
from sitebuilder.exception import SiteError
from zope.interface import implements, alsoProvides
import gtk


class ListControlAgent(object):
    """
    List main component control agent
    """
    implements(IActionObserver, ICommandObserver)

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
        elif action.name == ACTION_SUBMIT:
            self.submit_sites(parms['sites'])
        else:
            raise NotImplementedError("Unhandled action %s triggered" % action)

    def cb_reload_site_list(self, command):
        """
        A command has been executted and sites list should be refreshed
        """
        if command.status == COMMAND_SUCCESS:
            self.get_presentation_agent().load_widgets_data()
        else:
            print "command error: %s" % command.mesg

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def lookup_host_by_name(self, name, domain):
        """
        Retrieves all the configuraiton items from the abstraction
        """
        command = LookupHostByName("*", "*")
        enqueue_command(command)
        command.wait()

        if command.status == COMMAND_SUCCESS:
            return command.result
        else:
            raise command.exception

    def cb_show_detail_dialog_rw(self, command):
        """
        Command callback method to show detail dialog in read/write mode
        """
        if command.status == COMMAND_SUCCESS:
            site = command.result
            self.show_detail_dialog(site, False)
        else:
            raise command.exception

    def cb_show_detail_dialog_ro(self, command):
        """
        Command callback method to show detail dialog in read only mode
        """
        if command.status == COMMAND_SUCCESS:
            site = command.result
            self.show_detail_dialog(site, True)
        else:
            raise command.exception

    def show_detail_dialog(self, site, read_only=False):
        """
        Shows detail dialog for the specified site
        """
        detail = DetailMainControlAgent(site, read_only)

        if IActionSubject.providedBy(detail):
            detail.register_action_observer(self)

        presentation = detail.get_presentation_agent()
        presentation.show()

    def cb_show_delete_dialog(self, command):
        """
        Shows detail dialog for the specified site
        """
        if not  command.status == COMMAND_SUCCESS:
            raise command.exception

        conf_name = "%s.%s" % (command.name, command.domain)
        if not command.result:
            raise SiteError("Unknown site %s" % conf_name)

        if len(command.result) > 1:
            raise SiteError("Several sites named %s found" % conf_name)

        dnshost = command.result[0]

        dialog = gtk.MessageDialog(
            self.get_presentation_agent().get_toplevel(),
            #gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
            "Are you sure you want to delete configuraiton '%s' ?" % conf_name)

        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_YES:
            command = DeleteSite(dnshost.name, dnshost.domain)
            command.register_command_observer(self)
            enqueue_command(command)
            print "deleted site id %s" % conf_name

    def add_site(self):
        """
        Display detail dialog in add mode with a new site site
        """
        site = site_factory()
        alsoProvides(site, ISiteNew)
        self.show_detail_dialog(site)

    def view_selected_sites(self, selection):
        """
        Display detail dialog in view mode for each selected site id
        """
        for name, domain in selection:
            command = GetSiteByName(name, domain)
            command.register_command_callback(self.cb_show_detail_dialog_ro)
            enqueue_command(command)

    def edit_selected_sites(self, selection):
        """
        Display detail dialog in edit mode for each selected site id
        """
        for name, domain in selection:
            command = GetSiteByName(name, domain)
            command.register_command_callback(self.cb_show_detail_dialog_rw)
            enqueue_command(command)

    def delete_selected_sites(self, selection):
        """
        Display delete dialog for each selected site id
        """
        for name, domain in selection:
            if 1:
                conf_name = "%s.%s" % (name, domain)

                dialog = gtk.MessageDialog(
                    self.get_presentation_agent().get_toplevel(),
                    gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                    "Are you sure you want to delete configuraiton '%s' ?" % conf_name)

                response = dialog.run()
                dialog.destroy()

                if response == gtk.RESPONSE_YES:
                    command = DeleteSite(name, domain)
                    command.register_command_callback(self.cb_reload_site_list)
                    enqueue_command(command)
                    print "deleted site id %s" % conf_name

            else:
                command = LookupHostByName(name, domain)
                command.register_command_callback(self.cb_show_delete_dialog)
                enqueue_command(command)

    def submit_sites(self, sites):
        """
        Submits sites changes coming from detail compoenent to backend
        """
        for site in sites:
            if ISiteNew.providedBy(site):
                command = AddSite(site)
            else:
                command = UpdateSite(site)

            command.register_command_callback(self.cb_reload_site_list)
            enqueue_command(command)

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Destroyes presentation
        self._presentation_agent.register_action_observer(self)
        self._presentation_agent.destroy()


if __name__ == '__main__':

    from sitebuilder.application import init, uninit

    init()
    control = ListControlAgent()
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
    uninit()
