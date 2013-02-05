#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.event.events import UIActionEvent, UIWidgetEvent
from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.utils.parameters import ACTION_ADD, ACTION_VIEW
from sitebuilder.utils.parameters import ACTION_EDIT, ACTION_DELETE
from sitebuilder.utils.parameters import ACTION_RELOAD, ACTION_CLEARLOGS
from sitebuilder.utils.parameters import ACTION_SHOWLOGS
from sitebuilder.command.interface import COMMAND_SUCCESS
from sitebuilder.presentation.gtk.base import GtkBasePresentationAgent
from sitebuilder.observer.action import Action
from gobject import TYPE_PYOBJECT
from warnings import warn
import gtk


class ListMainPresentationAgent(GtkBasePresentationAgent):
    """
    ListPresentationAgent site add/edit/view interface.

    The interface design is loaded from a glade file.
    """
    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'list.glade')
    TOPLEVEL_NAME = "list"

    def load_widgets_data(self):
        """
        Loads site items data into widgets
        """
        pass


class ListSitesPresentationAgent(GtkBasePresentationAgent):
    """
    ListPresentationAgent site add/edit/view interface.

    The interface design is loaded from a glade file.
    """
    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'list_sites.glade')
    TOPLEVEL_NAME = "list"

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, control_agent)
        site_list = self['site_list']

        text_renderer = gtk.CellRendererText()

        cname = gtk.TreeViewColumn("Name", text_renderer, text=0)
        cname.set_sort_column_id(0)
        site_list.append_column(cname)

        cname = gtk.TreeViewColumn("Domain", text_renderer, text=1)
        cname.set_sort_column_id(1)
        site_list.append_column(cname)

        cplat = gtk.TreeViewColumn("Platform", text_renderer, text=2)
        cname.set_sort_column_id(2)
        site_list.append_column(cplat)

        cdesc = gtk.TreeViewColumn("Description", text_renderer, text=3)
        cname.set_sort_column_id(3)
        site_list.append_column(cdesc)

        hosts_model = gtk.ListStore(str, str, str, str)
        site_list.set_model(hosts_model)

        self['site_list'].connect('row-activated', self.on_site_list_row_activated)
        self['filter_name'].connect('changed', self.on_filter_name_changed)
        self['filter_domain'].connect('changed', self.on_filter_domain_changed)
        self['view'].connect('activate', self.on_view_activate)
        self['add'].connect('activate', self.on_add_activate)
        self['edit'].connect('activate', self.on_edit_activate)
        self['delete'].connect('activate', self.on_delete_activate)
        self['reload'].connect('activate', self.on_reload_activate)

    def set_value(self, name, hosts):
        """
        Loads site items data into widgets
        """
        # Appends items to the site_list
        sites_model = self['site_list'].get_model()

        if sites_model is None:
            warn("site_list has no model")
            sites_model = gtk.ListStore(str, str, str, str)
            self['site_list'].set_model(sites_model)

        sites_model.clear()

        for dnshost in hosts:
            name = dnshost.name
            domain = dnshost.domain
            platform = dnshost.platform
            description = dnshost.description
            sites_model.append((name, domain, platform, description))

    def get_value(self, name):
        """
        Returns the selected site identifier.

        As the treeview component used to display site list
        behaves exactly as a combobox item (thay share the same internal
        model), we may use the GtkBasePresentationAgent get_combobox_selection method
        to read it.
        """
        model, rows = self['site_list'].get_selection().get_selected_rows()
        selection = []

        for row in rows:
            index = row[0]
            name = model[index][0]
            domain = model[index][1]
            selection.append([name, domain])

        return selection

    def on_site_list_row_activated(self, widget, path, column):
        """
        Signal handler associated with the site_list tree view
        """
        self['view'].activate()

    def on_filter_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        name = self['filter_name'].get_text()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='filter_name', value=name))

    def on_filter_domain_changed(self, widget):
        """
        Signal handler associated with the template combobox
        """
        domain_name = self.get_combobox_selection(self['filter_domain'])
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='filter_domain', value=domain_name))

    def on_view_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.get_event_bus().publish(UIActionEvent(self, action=ACTION_VIEW))

    def on_add_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.get_event_bus().publish(UIActionEvent(self, action=ACTION_ADD))

    def on_edit_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.get_event_bus().publish(UIActionEvent(self, action=ACTION_EDIT))

    def on_delete_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.get_event_bus().publish(UIActionEvent(self, action=ACTION_DELETE))

    def on_reload_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.get_event_bus().publish(UIActionEvent(self, action=ACTION_RELOAD))

    def destroy(self):
        """
        Cleanly destroyes components
        """
        GtkBasePresentationAgent.destroy(self)


class ListLogsPresentationAgent(GtkBasePresentationAgent):
    """
    ListPresentationAgent site add/edit/view interface.

    The interface design is loaded from a glade file.
    """
    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'list_logs.glade')
    TOPLEVEL_NAME = "logs"

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, control_agent)
        img_renderer = gtk.CellRendererPixbuf()
        text_renderer = gtk.CellRendererText()
        logs_list = self['logs_list']

        #cdesc = gtk.TreeViewColumn("Command")
        #cdesc.pack_start(img_renderer, False)
        #cdesc.pack_start(text_renderer)
        #cdesc.set_sort_column_id(0)
        #logs_list.append_column(cdesc)

        cicon = gtk.TreeViewColumn("", img_renderer, stock_id=0)
        logs_list.append_column(cicon)

        cdesc = gtk.TreeViewColumn("Command", text_renderer, text=1)
        logs_list.append_column(cdesc)

        cres = gtk.TreeViewColumn("Result", text_renderer, text=2)
        logs_list.append_column(cres)

        logs_model = gtk.ListStore(str, str, str, TYPE_PYOBJECT)
        logs_list.set_model(logs_model)

        self['logs_list'].connect('row-activated', self.on_logs_list_row_activated)
        self['clearlogs'].connect('activate', self.on_clearlogs_activate)
        self['showlogs'].connect('activate', self.on_showlogs_activate)

    def set_items(self, name, commands):
        """
        Loads logs items data into widgets
        """
        # Appends items to the site_list
        model = self['logs_list'].get_model()
        model.clear()

        for command in commands:
            if command.status == COMMAND_SUCCESS:
                img = gtk.STOCK_OK
                text = command.mesg
            else:
                img = gtk.STOCK_CANCEL
                text = command.exception

            model.append((img, command.description, text, command))

    def get_selected_commands(self):
        """
        Returns the selected site identifier.

        As the treeview component used to display site list
        behaves exactly as a combobox item (thay share the same internal
        model), we may use the GtkBasePresentationAgent get_combobox_selection method
        to read it.
        """
        model, rows = self['logs_list'].get_selection().get_selected_rows()
        commands = []

        for row in rows:
            index = row[0]
            command = model[index][3]
            commands.append(command)

        return commands

    def on_logs_list_row_activated(self, widget, path, column):
        """
        Signal handler associated with the site_list tree view
        """
        self['showlogs'].activate()

    def on_clearlogs_activate(self, widget):
        """
        Signal handler associated with the clearlogs action
        """
        self.get_event_bus().publish(UIActionEvent(self, action=ACTION_CLEARLOGS))

    def on_showlogs_activate(self, widget):
        """
        Signal handler associated with the showlogs action
        """
        self.get_event_bus().publish(UIActionEvent(self, action=ACTION_SHOWLOGS,
            parameters={'logs': self.get_selected_commands()}))
