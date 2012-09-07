#!/usr/bin/env python
"""
Main list interface control agent
"""

from sitebuilder.presentation.gtk.list import ListMainPresentationAgent
from sitebuilder.presentation.gtk.list import ListSitesPresentationAgent
from sitebuilder.presentation.gtk.list import ListLogsPresentationAgent
from sitebuilder.control.base import BaseControlAgent
from sitebuilder.control.detail import DetailMainControlAgent
from sitebuilder.abstraction.site.factory import site_factory
from sitebuilder.presentation.interface import IPresentationAgent
from sitebuilder.observer.action import IActionObserver, IActionSubject
from sitebuilder.observer.command import ICommandObserver
from sitebuilder.command.interface import COMMAND_SUCCESS
from sitebuilder.abstraction.interface import ISiteNew
from sitebuilder.utils.parameters import ACTION_ADD, ACTION_VIEW, ACTION_SUBMIT
from sitebuilder.utils.parameters import ACTION_EDIT, ACTION_DELETE
from sitebuilder.utils.parameters import ACTION_RELOAD, ACTION_CLEARLOGS
from sitebuilder.utils.parameters import ACTION_SHOWLOGS
from sitebuilder.command.scheduler import enqueue_command
from sitebuilder.command.host import LookupHostByName
from sitebuilder.command.site import GetSiteByName, AddSite, UpdateSite
from sitebuilder.command.site import DeleteSite
from sitebuilder.observer.action import Action, ActionSubject
from sitebuilder.exception import SiteError, FieldFormatError
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from zope.interface import implements, alsoProvides
import gtk
import re


class ListMainControlAgent(object):
    """
    Site details main interface's control agent
    """
    implements(IActionObserver)

    def __init__(self):
        """
        ControlAgent initialization
        """
        presentation_agent = ListMainPresentationAgent(self)
        presentation_agent.register_action_observer(self)
        # Main detail presentation agent has no reason to listen to changed
        # attribute events. Disabled.
        # site.register_attribute_observer(presentation_agent)
        self._presentation_agent = presentation_agent

        # Creates sites list component
        slave = ListSitesControlAgent()
        self._sites_control_agent = slave
        presentation_agent = slave.get_presentation_agent()
        self._presentation_agent.attach_slave('sites', 'vbox_general',
                slave.get_presentation_agent())
        slave.register_action_observer(self)

        # Creates logs list component
        slave = ListLogsControlAgent()
        self._logs_control_agent = slave
        self._presentation_agent.attach_slave('logs', 'vbox_general',
                slave.get_presentation_agent())

        # Initial sites search (may be disabled id database is really big)
        self.reload_sites()

    def action_activated(self, action=None):
        """
        ActionActivatedObserver trigger mmethod local implementation
        """
        # Handles add action that do nat need any parameter
        if action.name == ACTION_ADD:
            self.add_site()
            return
        if action.name == ACTION_RELOAD:
            self.reload_sites()
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

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def set_presentation_agent(self, presentation_agent):
        """
        Sets local PresentationAgent implementation instance
        """
        # TODO: perform better instance check on presentation agent
        if not IPresentationAgent.providedBy(presentation_agent):
            raise AttributeError("presentation agent should implement " +
                                 "IPresentationAgent")

        self._presentation_agent = presentation_agent

    def show_detail_dialog(self, site, read_only=False):
        """
        Shows detail dialog for the specified site
        """
        detail = DetailMainControlAgent(site, read_only)

        if IActionSubject.providedBy(detail):
            detail.register_action_observer(self)

        presentation = detail.get_presentation_agent()
        presentation.show()

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
                command.register_command_callback(self.cb_reload_sites)
                command.register_command_observer(self._logs_control_agent)
                enqueue_command(command)
                print "deleted site id %s" % conf_name

    def submit_sites(self, sites):
        """
        Submits sites changes coming from detail component to backend
        """
        for site in sites:
            if ISiteNew.providedBy(site):
                command = AddSite(site)
            else:
                command = UpdateSite(site)

            command.register_command_callback(self.cb_reload_sites)
            command.register_command_observer(self._logs_control_agent)
            enqueue_command(command)

    def reload_sites(self):
        """
        Reloads site list by submitting a lookup query
        """
        sca = self._sites_control_agent
        filter_name = sca.get_value('filter_name')
        filter_domain = sca.get_value('filter_domain')

        command = LookupHostByName(filter_name, filter_domain)
        command.register_command_callback(self.cb_set_sites)
        enqueue_command(command)

    def cb_set_sites(self, command):
        """
        Site list has been reloaded and result has to be taken in account
        """
        sca = self._sites_control_agent

        if command.status == COMMAND_SUCCESS:
            sca.set_value('hosts', command.result)
        # TODO: manage error reporting for non logged commands

    def cb_reload_sites(self, command):
        """
        A command has been executted that needs sites list to be refreshed
        """
        if command.status == COMMAND_SUCCESS:
            self.reload_sites()
        # TODO: manage error reporting for non logged commands

    def cb_show_detail_dialog_rw(self, command):
        """
        Command callback method to show detail dialog in read/write mode
        """
        if command.status == COMMAND_SUCCESS:
            site = command.result
            self.show_detail_dialog(site, False)
        # TODO: manage error reporting for non logged commands

    def cb_show_detail_dialog_ro(self, command):
        """
        Command callback method to show detail dialog in read only mode
        """
        if command.status == COMMAND_SUCCESS:
            site = command.result
            self.show_detail_dialog(site, True)
        # TODO: manage error reporting for non logged commands

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


class ListSitesControlAgent(BaseControlAgent, ActionSubject):
    """
    List main component control agent
    """
    implements(IActionObserver)

    def __init__(self):
        """
        Initializes control agent.
        """
        BaseControlAgent.__init__(self)
        ActionSubject.__init__(self)
        self._hosts = []
        self._filter_name = '*'
        self._filter_name_re = re.compile(r"^[\w\d\*_-]*$")
        self._filter_domain = '*'
        self._filter_domain_re = re.compile(r"^[\w\d\*\._-]*$")
        pa  = ListSitesPresentationAgent(self)

        domains = SiteDefaultsManager.get_domains()
        domains['*'] =  '*'
        pa.set_items('filter_domain', domains)
        pa.register_action_observer(self)
        self.set_presentation_agent(pa)

    def get_value(self, name):
        """
        Returns a site attribute value
        """
        if name == "hosts":
            return self._hosts
        elif name == "filter_name":
            return self._filter_name
        elif name == "filter_domain":
            return self._filter_domain
        else:
            raise AttributeError("%s object has no attribute '%s'" % \
                                 (self.__class__.__name__, name))

    def set_value(self, name, value):
        """
        Returns a site attribute value
        """
        if name == "filter_name":
            if not self._filter_name_re.match(value):
                raise FieldFormatError("Invalid name filter. Should match /^[\w\d\*_-]*$/")
            # Atomatically appends * to name filter
            if not len(value):
                value = '*'
            elif len(value) and value[-1] != '*':
                value = '%s*' % value
            self._filter_name = value
            self.reload_sites()
        elif name == "filter_domain":
            if not self._filter_domain_re.match(value):
                raise FieldFormatError("Invalid name filter. Should match /^[\w\d\*\._-]*$/")
            self._filter_domain = value
            self.reload_sites()
        elif name == "hosts":
            self._hosts = value
            self.load_widgets_data()
        else:
            raise AttributeError("%s object has no attribute '%s'" % \
                                 (self.__class__.__name__, name))

    def load_widgets_data(self):
        """
        Roloads hosts list widget
        """
        sites = []

        for dnshost in self._hosts:
            name = dnshost.name
            domain = dnshost.domain
            platform = dnshost.platform
            description = dnshost.description
            sites.append((name, domain, platform, description))

        self.get_presentation_agent().set_items('site_list', sites)

    def reload_sites(self):
        """
        Asks parent control agent to reload sites
        """
        action = Action(ACTION_RELOAD)
        self.notify_action_activated(action)

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def action_activated(self, action):
        """
        Forwards actions to parent control agent
        """
        self.notify_action_activated(action)

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Destroyes presentation
        self._presentation_agent.remove_action_observer(self)
        self._presentation_agent.destroy()
        self.clear_action_observers()


class ListLogsControlAgent(object):
    """
    List main component control agent
    """
    implements(IActionObserver, ICommandObserver)

    def __init__(self):
        """
        Initializes control agent.
        """
        self._commands = []
        self._presentation_agent = ListLogsPresentationAgent(self)
        self._presentation_agent.register_action_observer(self)
        self.load_widgets_data()

    def load_widgets_data(self):
        """
        Loads logs items data into widgets
        """
        self._presentation_agent.set_items('logs_list', self._commands)

    def get_value(self, name):
        """
        Returns a site attribute value
        """
        pass

    def set_value(self, name, value):
        """
        Returns a site attribute value
        """
        pass

    def action_activated(self, action=None):
        """
        ActionActivatedObserver trigger mmethod local implementation
        """
        # Handles add action that do nat need any parameter
        if action.name == ACTION_CLEARLOGS:
            del (self._commands[:])
            self._presentation_agent.load_widgets_data()
        elif action.name == ACTION_SHOWLOGS:
            # Checks that ids parameter is correctly set in event parameters
            parms = action.parameters

            if not parms.has_key('logs'):
                raise AttributeError('logs parameter is not set in action parameters')

            for command in parms['logs']:
                self.show_command_result(command)
        else:
            raise NotImplementedError("Unhandled action %s triggered" % action)

    def show_command_result(self, command):
        """
        Show details on a command
        """
        if command.status == COMMAND_SUCCESS:
            text = "%s\n\nCommand status:\n\nCommand was successfully executed" % \
                    command.mesg
        else:
            text = ("%s\n\nCommand status:\n\nAn error occured: %s\n\n" + \
                   "Stack trace:\n\n%s") % \
                   (command.mesg, str(command.exception), command.traceback)

        dialog = gtk.MessageDialog(
            self.get_presentation_agent().get_toplevel(),
            gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
            text)

        dialog.run()
        dialog.destroy()

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def command_executed(self, command):
        """
        CommandObserver trigger mmethod local implementation
        """
        self._commands.append(command)
        self.load_widgets_data()

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Destroyes presentation
        self._presentation_agent.register_action_observer(self)
        self._presentation_agent.destroy()
        self.clear_log_observers()


if __name__ == '__main__':

    from sitebuilder.application import init, uninit

    init()
    control = ListMainControlAgent()
    presentation = control.get_presentation_agent()
    presentation.get_toplevel().connect("destroy", gtk.main_quit)
    presentation.show()
    gtk.main()
    uninit()
