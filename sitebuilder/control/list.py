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
from sitebuilder.command.interface import COMMAND_SUCCESS
from sitebuilder.abstraction.interface import ISiteNew
from sitebuilder.presentation.interface import IPresentationAgent
from sitebuilder.utils.parameters import ACTION_ADD, ACTION_VIEW, ACTION_SUBMIT
from sitebuilder.utils.parameters import ACTION_EDIT, ACTION_DELETE
from sitebuilder.utils.parameters import ACTION_RELOAD, ACTION_CLEARLOGS
from sitebuilder.utils.parameters import ACTION_SHOWLOGS
from sitebuilder.command.scheduler import enqueue_command
from sitebuilder.command.host import LookupHostByName
from sitebuilder.command.site import GetSiteByName, AddSite, UpdateSite
from sitebuilder.command.site import DeleteSite
from sitebuilder.exception import SiteError, FieldFormatError
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.event.events import UIActionEvent, AppActionEvent
from sitebuilder.event.events import UIWidgetEvent, CommandExecEvent
from zope.interface import alsoProvides
import re
import gtk


class ListMainControlAgent(object):
    """
    Site details main interface's control agent
    """

    def __init__(self):
        """
        ControlAgent initialization
        """
        pa = ListMainPresentationAgent(self)
        # Main detail presentation agent has no reason to listen to changed
        # attribute events. Disabled.
        # site.register_attribute_observer(presentation_agent)
        self._presentation_agent = pa

        # Creates sites list component
        slave = ListSitesControlAgent()
        self._sites_control_agent = slave
        self._presentation_agent.attach_slave('sites', 'vbox_general',
                                              slave.get_presentation_agent())
        # Listens for list sites controller action events
        slave.get_event_bus().subscribe(AppActionEvent,
                                        self.app_action_evt_callback)

        # Creates logs list component
        slave = ListLogsControlAgent()
        self._logs_control_agent = slave
        self._presentation_agent.attach_slave('logs', 'vbox_general',
                                              slave.get_presentation_agent())

        # Initial sites search (may be disabled id database is really big)
        self.reload_sites()

    def app_action_evt_callback(self, event):
        """
        Method triggerred on UIActionEvent
        """
        # Handles add action that do nat need any parameter
        if event.action == ACTION_ADD:
            self.add_site()
            return
        if event.action == ACTION_RELOAD:
            self.reload_sites()
            return

        # Checks that ids parameter is correctly set in event parameters
        parms = event.parameters

        if not 'sites' in parms:
            raise AttributeError('sites parameter is not set in action parameters')

        # Handles view action
        if event.action == ACTION_VIEW:
            self.view_selected_sites(parms['sites'])
        elif event.action == ACTION_EDIT:
            self.edit_selected_sites(parms['sites'])
        elif event.action == ACTION_DELETE:
            self.delete_selected_sites(parms['sites'])
        elif event.action == ACTION_SUBMIT:
            self.submit_sites(parms['sites'])
        else:
            raise NotImplementedError("Unhandled action %s triggered" % event.action)

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def set_presentation_agent(self, pa):
        """
        Sets local PresentationAgent implementation instance
        """
        # TODO: perform better instance check on presentation agent
        if not IPresentationAgent.providedBy(pa):
            raise AttributeError("presentation agent should implement " +
                                 "IPresentationAgent")

        self._presentation_agent = pa

    def show_detail_dialog(self, site, read_only=False):
        """
        Shows detail dialog for the specified site
        """
        detail = DetailMainControlAgent(site, read_only)
        detail.get_event_bus().subscribe(
            AppActionEvent, self.app_action_evt_callback)
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
            command.get_event_bus().subscribe(
                CommandExecEvent, self.cb_show_detail_dialog_ro)
            enqueue_command(command)

    def edit_selected_sites(self, selection):
        """
        Display detail dialog in edit mode for each selected site id
        """
        for name, domain in selection:
            command = GetSiteByName(name, domain)
            command.get_event_bus().subscribe(
                CommandExecEvent, self.cb_show_detail_dialog_rw)
            enqueue_command(command)

    def delete_selected_sites(self, selection):
        """
        Display delete dialog for each selected site id
        """
        for name, domain in selection:
            conf_name = "%s.%s" % (name, domain)

            # TODO: create a dedicated pac agent
            dialog = gtk.MessageDialog(
                self.get_presentation_agent().get_toplevel(),
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                "Are you sure you want to delete configuraiton '%s' ?" % conf_name)

            response = dialog.run()
            dialog.destroy()

            if response == gtk.RESPONSE_YES:
                command = DeleteSite(name, domain)
                command.get_event_bus().subscribe(CommandExecEvent,
                                                  self.cb_reload_sites)
                command.get_event_bus().subscribe(
                    CommandExecEvent,
                    self._logs_control_agent.command_evt_callback)
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

            command.get_event_bus().subscribe(
                CommandExecEvent, self.cb_reload_sites)

            command.get_event_bus().subscribe(
                CommandExecEvent,
                self._logs_control_agent.command_evt_callback)

            enqueue_command(command)

    def reload_sites(self):
        """
        Reloads site list by submitting a lookup query
        """
        sca = self._sites_control_agent
        filter_name = sca.get_value('filter_name')
        filter_domain = sca.get_value('filter_domain')

        command = LookupHostByName(filter_name, filter_domain)
        command.get_event_bus().subscribe(CommandExecEvent,
                                          self.cb_set_sites)
        enqueue_command(command)

    def cb_set_sites(self, event):
        """
        Site list has been reloaded and result has to be taken in account
        """
        command = event.source
        sca = self._sites_control_agent

        if command.status == COMMAND_SUCCESS:
            sca.set_value('hosts', command.result)
        # TODO: manage error reporting for non logged commands

    def cb_reload_sites(self, event):
        """
        A command has been executted that needs sites list to be refreshed
        """
        command = event.source

        if command.status == COMMAND_SUCCESS:
            self.reload_sites()
        # TODO: manage error reporting for non logged commands

    def cb_show_detail_dialog_rw(self, event):
        """
        Command callback method to show detail dialog in read/write mode
        """
        command = event.source

        if command.status == COMMAND_SUCCESS:
            site = command.result
            self.show_detail_dialog(site, False)
        # TODO: manage error reporting for non logged commands

    def cb_show_detail_dialog_ro(self, event):
        """
        Command callback method to show detail dialog in read only mode
        """
        command = event.source

        if command.status == COMMAND_SUCCESS:
            site = command.result
            self.show_detail_dialog(site, True)
        # TODO: manage error reporting for non logged commands

    def cb_show_delete_dialog(self, event):
        """
        Shows detail dialog for the specified site
        """
        command = event.source

        if not command.status == COMMAND_SUCCESS:
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


class ListSitesControlAgent(BaseControlAgent):
    """
    List main component control agent
    """

    def __init__(self):
        """
        Initializes control agent.
        """
        BaseControlAgent.__init__(self)
        self._hosts = []
        self._filter_name = '*'
        self._filter_name_re = re.compile(r"^[\w\d\*_-]*$")
        self._filter_domain = '*'
        self._filter_domain_re = re.compile(r"^[\w\d\*\._-]*$")
        pa = ListSitesPresentationAgent(self)

        domains = SiteDefaultsManager.get_domains()
        domains['*'] = '*'
        pa.set_items('filter_domain', domains)
        pa.get_event_bus().subscribe(UIActionEvent, self.action_evt_callback)
        pa.get_event_bus().subscribe(UIWidgetEvent, self.widget_evt_callback)
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
            raise AttributeError("%s object has no attribute '%s'" %
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
            raise AttributeError("%s object has no attribute '%s'" %
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

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def action_evt_callback(self, event):
        """
        Forwards actions to parent control agent
        """
        pa = self.get_presentation_agent()

        if event.action in (ACTION_VIEW, ACTION_EDIT, ACTION_DELETE):
            self.get_event_bus().publish(
                AppActionEvent(self, action=event.action,
                    parameters={'sites': pa.get_value('site_list')}))

        elif event.action in (ACTION_ADD, ACTION_RELOAD):
            self.get_event_bus().publish(AppActionEvent(self, action=event.action))
        else:
            raise NotImplementedError("Unhandled action %d triggered" %
                                      event.action)

    def widget_evt_callback(self, event):
        """
        """
        pa = self.get_presentation_agent()

        try:
            self.set_value(event.name, event.value)
        except (FieldFormatError), e:
            pa.set_error(event.name, True, str(e))
        else:
            pa.set_error(event.name, False)

    def reload_sites(self):
        """
        Sends an ACTION_RELOAD action to reload sites.
        """
        self.get_event_bus().publish(AppActionEvent(self, action=ACTION_RELOAD))

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

    def __init__(self):
        """
        Initializes control agent.
        """
        self._commands = []
        pa = ListLogsPresentationAgent(self)
        pa.get_event_bus().subscribe(UIActionEvent, self.action_evt_callback)
        self._presentation_agent = pa
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

    def action_evt_callback(self, event):
        """
        ActionActivatedObserver trigger mmethod local implementation
        """
        # Handles add action that do nat need any parameter
        if event.action == ACTION_CLEARLOGS:
            del (self._commands[:])
            self.load_widgets_data()
        elif event.action == ACTION_SHOWLOGS:
            # Checks that ids parameter is correctly set in event parameters
            parms = event.parameters

            if not 'logs' in parms:
                raise AttributeError('logs parameter is not set in action parameters')

            for command in parms['logs']:
                self.show_command_result(command)
        else:
            raise NotImplementedError("Unhandled action %s triggered" % event.action)

    def show_command_result(self, command):
        """
        Show details on a command
        """
        if command.status == COMMAND_SUCCESS:
            text = "%s\n\nCommand status:\n\nCommand was successfully executed" % \
                command.mesg
        else:
            text = ("%s\n\nCommand status:\n\nAn error occured: %s\n\n" + \
                "Stack trace:\n\n%s") % (command.mesg, str(command.exception),
                command.traceback)

        dialog = gtk.MessageDialog(
            self.get_presentation_agent().get_toplevel(),
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
            text)

        dialog.run()
        dialog.destroy()

    def get_presentation_agent(self):
        """
        Returns ListPresentationAgent presentation instance
        """
        return self._presentation_agent

    def command_evt_callback(self, event):
        """
        CommandObserver trigger mmethod local implementation
        """
        self._commands.append(event.source)
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
