#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.utils.parameters import ACTION_ADD, ACTION_VIEW
from sitebuilder.utils.parameters import ACTION_EDIT, ACTION_DELETE
from sitebuilder.utils.parameters import ACTION_RELOAD
from sitebuilder.presentation.gtk.base import GtkBasePresentationAgent
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.observer.action import Action
from sitebuilder.interfaces.log import ILogObserver
from zope.interface import implements
from warnings import warn
import gtk

class ListPresentationAgent(GtkBasePresentationAgent):
    """
    ListPresentationAgent site add/edit/view interface.

    The interface design is loaded from a glade file.
    """
    implements(ILogObserver)

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'list.glade')
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

        log_list = self['log_list']

        cfname = gtk.TreeViewColumn("Event", text_renderer, text=0)
        cfname.set_sort_column_id(0)
        log_list.append_column(cfname)

        log_model = gtk.ListStore(str)
        log_list.set_model(log_model)

        domains = SiteDefaultsManager.get_domains()
        domains['*'] = '*'
        self.set_combobox_items(self['filter_domain'], domains)
        self['filter_domain'].set_active(0)

        self.load_widgets_data()

        self['site_list'].connect('row-activated', self.on_site_list_row_activated)
        self['filter_name'].connect('changed', self.on_filter_name_changed)
        self['filter_domain'].connect('changed', self.on_filter_domain_changed)
        self['view'].connect('activate', self.on_view_activate)
        self['add'].connect('activate', self.on_add_activate)
        self['edit'].connect('activate', self.on_edit_activate)
        self['delete'].connect('activate', self.on_delete_activate)
        self['reload'].connect('activate', self.on_reload_activate)

    def load_widgets_data(self):
        """
        Loads site items data into widgets
        """
        # Appends items to the site_list
        model = self['site_list'].get_model()

        if model is None:
            warn("site_list has no model")
            model = gtk.ListStore(str, str, str, str)
            self['site_list'].set_model(model)

        # FIXME: problem on reloding sites
        model.clear()
        hosts = self.get_control_agent().get_attribute_value('hosts')

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

    def on_filter_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        self.set_entry_attribute(widget, 'filter_name', True)

    def on_filter_domain_changed(self, widget):
        """
        Signal handler associated with the template combobox
        """
        domain_name = self.get_combobox_selection(self['filter_domain'])
        self.get_control_agent().set_attribute_value('filter_domain', domain_name )

    def on_view_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            Action(ACTION_VIEW, {'sites': self.get_selected_items()}))

    def on_add_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(Action(ACTION_ADD))

    def on_edit_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            Action(ACTION_EDIT, {'sites': self.get_selected_items()}))

    def on_delete_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(
            Action(ACTION_DELETE, {'sites': self.get_selected_items()}))

    def on_reload_activate(self, widget):
        """
        Signal handler associated with the view action
        """
        self.notify_action_activated(Action(ACTION_RELOAD))

    def event_logged(self, text):
        """
        LogObserver trigger mmethod local implementation
        """
        # Appends items to the site_list
        model = self['log_list'].get_model()

        if model is None:
            warn("log_list has no model")
            model = gtk.ListStore(str)
            self['log_list'].set_model(model)

        model.append((text,))
        self["statusbar"].push(0, text)

    def destroy(self):
        """
        Cleanly destroyes components
        """
        GtkBasePresentationAgent.destroy(self)
