#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.presentation.gtk.base import GtkBasePresentationAgent
from sitebuilder.event.events import UIActionEvent, UIWidgetEvent
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
        self._validity_matrix = {}

    def on_submit_activate(self, widget):
        """
        Signal handler associated with the submit action
        """
        self.get_event_bus().publish(
            UIActionEvent(self, action=ACTION_SUBMIT))

    def on_cancel_activate(self, widget):
        """
        Signal handler associated with the canhcel action
        """
        self.get_event_bus().publish(
            UIActionEvent(self, action=ACTION_CANCEL))


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
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['maintenance'].connect('toggled', self.on_maintenance_toggled)
        self['template'].connect('changed', self.on_template_changed)
        self['access'].connect('changed', self.on_access_changed)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='enabled', value=enabled))

    def on_maintenance_toggled(self, widget):
        """
        Signal handler associated with the maintenance checkbox
        """
        maintenance = self['maintenance'].get_active()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='maintenance', value=maintenance))

    def on_template_changed(self, widget):
        """
        Signal handler associated with the template combobox
        """
        template = self.get_combobox_selection(self['template'])
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='template', value=template))

    def on_access_changed(self, widget):
        """
        Signal handler associated with the access combobox
        """
        access = self.get_combobox_selection(self['access'])
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='access', value=access))


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
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='enabled', value=enabled) )

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        name = self['name'].get_text()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='name', value=name) )

    def on_username_changed(self, widget):
        """
        Signal handler associated with the username text input
        """
        username = self['username'].get_text()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='username', value=username) )

    def on_password_changed(self, widget):
        """
        Signal handler associated with the password text input
        """
        password = self['password'].get_text()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='password', value=password) )

    def on_type_changed(self, widget):
        """
        Signal handler associated with the type combobox
        """
        dbtype = self.get_value('type')
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='type', value=dbtype) )


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
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='enabled', value=enabled) )

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        name = self['name'].get_text()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='name', value=name) )

    def on_type_changed(self, widget):
        """
        Signal handler associated with the type combobox
        """
        repotype = self.get_value('type')
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='type', value=repotype) )


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
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='name', value=name) )

    def on_description_changed(self, widget):
        """
        Signal handler associated with the description text input
        """
        description = self['description'].get_text()
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='description', value=description) )

    def on_domain_changed(self, widget):
        """
        Signal handler associated with the domain combobox
        """
        domain = self.get_combobox_selection(self['domain'])
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='domain', value=domain) )

    def on_platform_changed(self, widget):
        """
        Signal handler associated with the platform combobox
        """
        platform = self.get_combobox_selection(self['platform'])
        self.get_event_bus().publish(
            UIWidgetEvent(self, name='platform', value=platform) )
