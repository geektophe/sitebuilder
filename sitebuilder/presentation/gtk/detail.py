#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.presentation.gtk.base import GtkBasePresentationAgent
from sitebuilder.abstraction.site.defaults import SiteDefaultsManager
from sitebuilder.observer.action import Action
from sitebuilder.utils.parameters import ACTION_SUBMIT, ACTION_CANCEL

class DetailMainPresentationAgent(GtkBasePresentationAgent):
    """
    DetailMainPresentationAgent site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit.glade')
    TOPLEVEL_NAME = "main"

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, control_agent)
        self['submit'].connect('activate', self.on_submit_activate)
        self['cancel'].connect('activate', self.on_cancel_activate)
        self.get_toplevel().connect('destroy', self.on_cancel_activate)
        #self.set_submit_state(False)
        self._validity_matrix = {}

    def on_submit_activate(self, widget):
        """
        Signal handler associated with the submit action
        """
        self.notify_action_activated(Action(ACTION_SUBMIT))

    def on_cancel_activate(self, widget):
        """
        Signal handler associated with the canhcel action
        """
        self.notify_action_activated(Action(ACTION_CANCEL))


class DetailSitePresentationAgent(GtkBasePresentationAgent):
    """
    Detail site presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_site.glade')
    TOPLEVEL_NAME = "site"

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, control_agent)

        # Sets widgets signal handlers
        #self._builder.connect_signals(self)
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['maintenance'].connect('toggled', self.on_maintenance_toggled)
        self['template'].connect('changed', self.on_template_changed)
        self['access'].connect('changed', self.on_access_changed)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        #self.get_control_agent().set_attribute_value('enabled', enabled)
        self.notify_widget_changed('enabled', enabled)

    def on_maintenance_toggled(self, widget):
        """
        Signal handler associated with the maintenance checkbox
        """
        maintenance = self['maintenance'].get_active()
        #self.get_control_agent().set_attribute_value('maintenance', maintenance)
        self.notify_widget_changed('maintenance', maintenance)

    def on_template_changed(self, widget):
        """
        Signal handler associated with the template combobox
        """
        #self.set_combobox_attribute(widget, 'template')
        template = self.get_combobox_selection(self['template'])
        self.notify_widget_changed('template', template)

    def on_access_changed(self, widget):
        """
        Signal handler associated with the access combobox
        """
        #self.set_combobox_attribute(widget, 'access')
        access = self.get_combobox_selection(self['access'])
        self.notify_widget_changed('access', access)


class DetailDatabasePresentationAgent(GtkBasePresentationAgent):
    """
    Detail database presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_db.glade')
    TOPLEVEL_NAME = "database"

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, control_agent)
        # Sets widgets signal handlers
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['name'].connect('changed', self.on_name_changed)
        self['username'].connect('changed', self.on_username_changed)
        self['password'].connect('changed', self.on_password_changed)
        self['type'].connect('changed', self.on_type_changed)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        #self.get_control_agent().set_attribute_value('enabled', enabled)
        self.notify_widget_changed('enabled', enabled)

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        #self.set_entry_attribute(widget, 'name', False)
        name = self['name'].get_text()
        self.notify_widget_changed('name', name)

    def on_username_changed(self, widget):
        """
        Signal handler associated with the username text input
        """
        #self.set_entry_attribute(widget, 'username', False)
        username = self['username'].get_text()
        self.notify_widget_changed('username', username)

    def on_password_changed(self, widget):
        """
        Signal handler associated with the password text input
        """
        #self.set_entry_attribute(widget, 'password')
        password = self['password'].get_text()
        self.notify_widget_changed('password', password)

    def on_type_changed(self, widget):
        """
        Signal handler associated with the type combobox
        """
        #self.set_combobox_attribute(widget, 'type')
        dbtype = self.get_combobox_selection(self['type'])
        self.notify_widget_changed('type', dbtype)


class DetailRepositoryPresentationAgent(GtkBasePresentationAgent):
    """
    Detail repository presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_repo.glade')
    TOPLEVEL_NAME = "repository"

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, control_agent)

        # Sets widgets signal handlers
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['name'].connect('changed', self.on_name_changed)
        self['type'].connect('changed', self.on_type_changed)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        self.notify_widget_changed('enabled', enabled)

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        name = self['name'].get_text()
        self.notify_widget_changed('name', name)

    def on_type_changed(self, widget):
        """
        Signal handler associated with the type combobox
        """
        repotype = self.get_combobox_selection(self['type'])
        self.notify_widget_changed('type', repotype)


class DetailDNSHostPresentationAgent(GtkBasePresentationAgent):
    """
    Detail general presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_dnshost.glade')
    TOPLEVEL_NAME = "dnshost"

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, control_agent)

        # Sets widgets signal handlers
        self['description'].connect('changed', self.on_description_changed)
        self['name'].connect('changed', self.on_name_changed)
        self['domain'].connect('changed', self.on_domain_changed)
        self['platform'].connect('changed', self.on_platform_changed)

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        name = self['name'].get_text()
        self.notify_widget_changed('name', name)

    def on_description_changed(self, widget):
        """
        Signal handler associated with the description text input
        """
        description = self['description'].get_text()
        self.notify_widget_changed('description', description)

    def on_domain_changed(self, widget):
        """
        Signal handler associated with the domain combobox
        """
        domain = self.get_combobox_selection(self['domain'])
        self.notify_widget_changed('domain', domain)

    def on_platform_changed(self, widget):
        """
        Signal handler associated with the platform combobox
        """
        platform = self.get_combobox_selection(self['platform'])
        self.notify_widget_changed('platform', platform)
