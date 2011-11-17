#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
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

        cname = gtk.TreeViewColumn("Name", renderer, text=1)
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
        Loads configuration items data into widgets
        """

        # Appends items to the site_list
        model = self['site_list'].get_model()
        model.clear()
        sites = self.get_control_agent().get_configuration_all()
        i = 0

        for site in sites:
            dnshost = site.dnshost
            identifier = i
            name = dnshost.name
            domain = dnshost.domain
            fqdn = "%s.%s" % (name, domain)
            platform = dnshost.platform
            description = dnshost.description
            model.append((identifier, fqdn, platform, description))
            i += 1

    def get_selected_items(self):
        """
        Returns the selected configuration identifier.

        As the treeview component used to display configuration list
        behaves exactly as a combobox item (thay share the same internal
        model), we may use the GtkBasePresentationAgent get_combobox_selection method
        to read it.
        """
        model, rows = self['site_list'].get_selection().get_selected_rows()
        selection = []

        for row in rows:
            index = row[0]
            identifier = int(model[index][0])
            selection.append(identifier)

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
            ActionActivatedEvent('view', {'ids': self.get_selected_items()}))

    def on_add_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(ActionActivatedEvent('add'))

    def on_edit_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            ActionActivatedEvent('edit', {'ids': self.get_selected_items()}))

    def on_delete_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            ActionActivatedEvent('delete', {'ids': self.get_selected_items()}))

    def destroy(self):
        """
        Cleanly destroyes components
        """
        GtkBasePresentationAgent.destroy(self)
