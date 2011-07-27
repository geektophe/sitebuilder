#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.view.gtk.base import GtkBaseView
from sitebuilder.utils.observer import ViewActionDispatcher
from sitebuilder.utils.observer import AddActionDispatcher
from sitebuilder.utils.observer import EditActionDispatcher
from sitebuilder.utils.observer import DeleteActionDispatcher
import gtk

class ListView(GtkBaseView, ViewActionDispatcher, AddActionDispatcher,
              EditActionDispatcher, DeleteActionDispatcher):
    """
    ListView site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'list.glade')

    def __init__(self, controller):
        """
        Class initialization.
        """
        GtkBaseView.__init__(self, 'list', controller)
        ViewActionDispatcher.__init__(self)
        AddActionDispatcher.__init__(self)
        EditActionDispatcher.__init__(self)
        DeleteActionDispatcher.__init__(self)
        site_list = self['site_list']

        model = gtk.ListStore(str, str, str)
        site_list.set_model(model)
        renderer = gtk.CellRendererText()

        cname = gtk.TreeViewColumn("Name", renderer, text=1)
        cname.set_sort_column_id(1)
        site_list.append_column(cname)

        cdesc = gtk.TreeViewColumn("Description", renderer, text=2)
        cname.set_sort_column_id(2)
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
        sites = self._controller.get_configuration_all()

        for site in sites:
            general = site.get_attribute('general')
            identifier = general.get_attribute('id').get_value()
            name = general.get_attribute('name').get_value()
            description = general.get_attribute('description').get_value()
            model.append((identifier, name, description))

    def get_selected_items(self):
        """
        Returns the selected configuration identifier.

        As the treeview component used to display configuration list
        behaves exactly as a combobox item (thay share the same internal
        model), we may use the GtkBaseView get_combobox_selection method
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
        self.notify_view_action_activated()

    def on_add_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_add_action_activated()

    def on_edit_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_edit_action_activated()

    def on_delete_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_delete_action_activated()

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Clears listeners lists
        self.clear_add_action_activated_listeners()
        self.clear_view_action_activated_listeners()
        self.clear_edit_action_activated_listeners()
        self.clear_delete_action_activated_listeners()
        GtkBaseView.destroy(self)
