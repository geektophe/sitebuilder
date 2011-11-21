#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.utils.parameters import ACTION_ADD, ACTION_VIEW
from sitebuilder.utils.parameters import ACTION_EDIT, ACTION_DELETE
from sitebuilder.presentation.gtk.base import GtkBasePresentationAgent
from sitebuilder.observer.action import ActionActivatedEvent
import gtk

class ListPresentationAgent(GtkBasePresentationAgent):
    """
    ListPresentationAgent site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'list.glade')

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, 'list', control_agent)
        site_list = self['site_list']

        model = gtk.ListStore(str, str, str, str)
        site_list.set_model(model)
        renderer = gtk.CellRendererText()

        cname = gtk.TreeViewColumn("Name", renderer, text=0)
        cname.set_sort_column_id(0)
        site_list.append_column(cname)

        cname = gtk.TreeViewColumn("Domain", renderer, text=1)
        cname.set_sort_column_id(1)
        site_list.append_column(cname)

        cdesc = gtk.TreeViewColumn("Platform", renderer, text=2)
        cname.set_sort_column_id(2)
        site_list.append_column(cdesc)

        cdesc = gtk.TreeViewColumn("Description", renderer, text=3)
        cname.set_sort_column_id(3)
        site_list.append_column(cdesc)

        self.load_widgets_data()

        self['site_list'].connect('row-activated', self.on_site_list_row_activated)
        self['view'].connect('activate', self.on_view_activate)
        self['add'].connect('activate', self.on_add_activate)
        self['edit'].connect('activate', self.on_edit_activate)
        self['delete'].connect('activate', self.on_delete_activate)

    def load_widgets_data(self):
        """
        Loads site items data into widgets
        """

        # Appends items to the site_list
        model = self['site_list'].get_model()
        model.clear()
        hosts = self.get_control_agent().lookup_host_by_name("*", "*")

        for dnshost in hosts:
            name = dnshost.name
            domain = dnshost.domain
            platform = dnshost.platform
            description = dnshost.description
            model.append((name, domain, platform, description))

    def get_selected_items(self):
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

    def on_view_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            ActionActivatedEvent(ACTION_VIEW, {'sites': self.get_selected_items()}))

    def on_add_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(ActionActivatedEvent(ACTION_ADD))

    def on_edit_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            ActionActivatedEvent(ACTION_EDIT, {'sites': self.get_selected_items()}))

    def on_delete_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            ActionActivatedEvent(ACTION_DELETE, {'sites': self.get_selected_items()}))

    def destroy(self):
        """
        Cleanly destroyes components
        """
        GtkBasePresentationAgent.destroy(self)
