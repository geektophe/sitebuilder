#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.observer.datachanged import DataChangedListener
from sitebuilder.observer.submitaction import SubmitActionDispatcher
from sitebuilder.observer.cancelaction import CancelActionDispatcher
from sitebuilder.presentation.gtk.base import GtkBasePresentationAgent
from sitebuilder.abstraction.site import SiteConfigurationManager

class DetailMainPresentationAgent(GtkBasePresentationAgent,
                                  SubmitActionDispatcher,
                                  CancelActionDispatcher):
    """
    DetailMainPresentationAgent site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit.glade')

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, 'main', control_agent)
        SubmitActionDispatcher.__init__(self)
        CancelActionDispatcher.__init__(self)
        self['submit'].connect('activate', self.on_submit_activate)
        self['cancel'].connect('activate', self.on_cancel_activate)
        self.get_toplevel().connect('destroy', self.on_cancel_activate)

    def set_submit_state(self, flag):
        """
        Enables or disabled OK button depending on flag state
        """
        self['submit'].set_sensitive(flag)

    def on_submit_activate(self, widget):
        """
        Signal handler associated with the submit action
        """
        self.notify_submit_action_activated()

    def on_cancel_activate(self, widget):
        """
        Signal handler associated with the canhcel action
        """
        self.notify_cancel_action_activated()

    def destroy(self):
        """
        Cleanly destroyes components
        """
        # Clears listeners lists
        self.clear_submit_action_activated_listeners()
        self.clear_cancel_action_activated_listeners()
        GtkBasePresentationAgent.destroy(self)


class DetailSitePresentationAgent(GtkBasePresentationAgent,
                                  DataChangedListener):
    """
    Detail site presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_site.glade')

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, 'site', control_agent)

        # Listens data changed events from from control agent
        control_agent.add_data_changed_listener(self)

        # Sets widgets signal handlers
        #self._builder.connect_signals(self)
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['maintenance'].connect('toggled', self.on_maintenance_toggled)
        self['template'].connect('changed', self.on_template_changed)
        self['access'].connect('changed', self.on_access_changed)

        # Loads comboboxes items
        self.set_combobox_items(self['template'],
                SiteConfigurationManager.get_site_templates())
        self.set_combobox_items(self['access'],
                SiteConfigurationManager.get_site_accesses())

        # Loads widgets data from control agent
        self.load_widgets_data()

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the control agent
        """
        return self.get_control_agent().get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the control agent
        """
        self.get_control_agent().set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        enabled = self.get_attribute_value('enabled')
        done = self.get_attribute_value('done')
        read_only = self.get_control_agent().get_read_only_flag()
        sensitive = enabled and not done and not read_only

        # Loads enabled checkbox state
        self['enabled'].set_active(enabled)
        self['enabled'].set_sensitive(not done and not read_only)

        # Loads maintenance checkbox state
        maintenance = self.get_attribute_value('maintenance')
        self['maintenance'].set_active(maintenance)
        # Maintenance should be changeable even if site is in done state
        self['maintenance'].set_sensitive(enabled and not read_only)

        # Loads template combobox selected option
        self.set_combobox_selection(self['template'],
                self.get_attribute_value('template'))
        self['template'].set_sensitive(sensitive)

        # Loads access combobox selected option
        self.set_combobox_selection(self['access'],
                self.get_attribute_value('access'))
        # Access should be changeable even if site is in done state
        self['access'].set_sensitive(enabled and not read_only)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        self.set_attribute_value('enabled', enabled)

    def on_maintenance_toggled(self, widget):
        """
        Signal handler associated with the maintenance checkbox
        """
        maintenance = self['maintenance'].get_active()
        self.set_attribute_value('maintenance', maintenance)

    def on_template_changed(self, widget):
        """
        Signal handler associated with the template combobox
        """
        template_name = self.get_combobox_selection(self['template'])
        self.set_attribute_value('template', template_name )

    def on_access_changed(self, widget):
        """
        Signal handler associated with the access combobox
        """
        access = self.get_combobox_selection(self['access'])
        self.set_attribute_value('access', access )

    def destroy(self):
        """
        Cleanly destroyes components
        """
        self.get_control_agent().remove_data_changed_listener(self)
        GtkBasePresentationAgent.destroy(self)


class DetailDatabasePresentationAgent(GtkBasePresentationAgent,
                                      DataChangedListener):
    """
    Detail database presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_db.glade')

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, 'database',
                                              control_agent)

        # Listens data changed events from from control agent
        control_agent.add_data_changed_listener(self)

        # Sets widgets signal handlers
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['name'].connect('changed', self.on_name_changed)
        self['username'].connect('changed', self.on_username_changed)
        self['password'].connect('changed', self.on_password_changed)
        self['type'].connect('changed', self.on_type_changed)

        # Loads comboboxes items
        self.set_combobox_items(self['type'],
                SiteConfigurationManager.get_database_types())

        # Loads widgets data from control agent
        self.load_widgets_data()

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the control agent
        """
        return self.get_control_agent().get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the control agent
        """
        self.get_control_agent().set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        enabled = self.get_attribute_value('enabled')
        done = self.get_attribute_value('done')
        read_only = self.get_control_agent().get_read_only_flag()
        sensitive = enabled and not done and not read_only

        name = self.get_attribute_value('name')
        username = self.get_attribute_value('username')
        password = self.get_attribute_value('password')

        # Loads enabled checkbox state
        self['enabled'].set_active(enabled)
        self['enabled'].set_sensitive(not done and not read_only)

        # Loads name entry
        self['name'].set_text(name)
        self['name'].set_sensitive(sensitive)

        # Loads username entry
        self['username'].set_text(username)
        self['username'].set_sensitive(sensitive)

        # Loads password entry
        self['password'].set_text(password)
        self['password'].set_sensitive(sensitive)

        # Loads type combobox selected option
        self.set_combobox_selection(self['type'],
                self.get_attribute_value('type'))
        self['type'].set_sensitive(sensitive)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        self.set_attribute_value('enabled', enabled)

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        self.set_entry_attribute(widget, 'name')

    def on_username_changed(self, widget):
        """
        Signal handler associated with the username text input
        """
        self.set_entry_attribute(widget, 'username')

    def on_password_changed(self, widget):
        """
        Signal handler associated with the password text input
        """
        self.set_entry_attribute(widget, 'password')

    def on_type_changed(self, widget):
        """
        Signal handler associated with the type combobox
        """
        type_name = self.get_combobox_selection(self['type'])
        self.set_attribute_value('type', type_name )

    def destroy(self):
        """
        Cleanly destroyes components
        """
        self.get_control_agent().remove_data_changed_listener(self)
        GtkBasePresentationAgent.destroy(self)


class DetailRepositoryPresentationAgent(GtkBasePresentationAgent,
                                        DataChangedListener):
    """
    Detail repository presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_repo.glade')

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, 'repository', control_agent)

        # Listens data changed events from from control agent
        control_agent.add_data_changed_listener(self)

        # Sets widgets signal handlers
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['name'].connect('changed', self.on_name_changed)
        self['type'].connect('changed', self.on_type_changed)

        # Loads comboboxes items
        self.set_combobox_items(self['type'],
                SiteConfigurationManager.get_repository_types())

        # Loads widgets data from control agent
        self.load_widgets_data()

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the control agent
        """
        return self.get_control_agent().get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the control agent
        """
        self.get_control_agent().set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        enabled = self.get_attribute_value('enabled')
        done = self.get_attribute_value('done')
        read_only = self.get_control_agent().get_read_only_flag()
        sensitive = enabled and not done and not read_only

        name = self.get_attribute_value('name')

        # Loads enabled checkbox state
        self['enabled'].set_active(enabled)
        self['enabled'].set_sensitive(not done and not read_only)

        # Loads name entry
        self['name'].set_text(name)
        self['name'].set_sensitive(sensitive)

        # Loads type combobox selected option
        self.set_combobox_selection(self['type'],
                self.get_attribute_value('type'))
        self['type'].set_sensitive(sensitive)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        self.set_attribute_value('enabled', enabled)

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        self.set_entry_attribute(widget, 'name')

    def on_type_changed(self, widget):
        """
        Signal handler associated with the type combobox
        """
        type_name = self.get_combobox_selection(self['type'])
        self.set_attribute_value('type', type_name )

    def destroy(self):
        """
        Cleanly destroyes components
        """
        self.get_control_agent().remove_data_changed_listener(self)
        GtkBasePresentationAgent.destroy(self)


class DetailGeneralPresentationAgent(GtkBasePresentationAgent,
                                     DataChangedListener):
    """
    Detail general presentation agent composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_general.glade')

    def __init__(self, control_agent):
        """
        Class initialization.
        """
        GtkBasePresentationAgent.__init__(self, 'general', control_agent)

        # Listens data changed events from from control agent
        control_agent.add_data_changed_listener(self)

        # Sets widgets signal handlers
        self['description'].connect('changed', self.on_description_changed)
        self['name'].connect('changed', self.on_name_changed)
        self['domain'].connect('changed', self.on_domain_changed)
        self['platform'].connect('changed', self.on_platform_changed)

        # Loads comboboxes items
        self.set_combobox_items(self['domain'],
                SiteConfigurationManager.get_domains())
        self.set_combobox_items(self['platform'],
                SiteConfigurationManager.get_platforms())

        # Loads widgets data from control agent
        self.load_widgets_data()

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the control agent
        """
        return self.get_control_agent().get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the control agent
        """
        self.get_control_agent().set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates presentation agent widgets based on configuraton settings
        """
        read_only = self.get_control_agent().get_read_only_flag()
        done = self.get_attribute_value('done')
        sensitive = not done and not read_only
        name = self.get_attribute_value('name')
        description = self.get_attribute_value('description')

        # Loads name entry
        self['name'].set_text(name)
        self['name'].set_sensitive(sensitive)

        # Loads description entry
        self['description'].set_text(description)
        self['description'].set_sensitive(sensitive)

        # Loads domain combobox selected option
        self.set_combobox_selection(self['domain'],
                self.get_attribute_value('domain'))
        self['domain'].set_sensitive(sensitive)

        # Loads platform combobox selected option
        self.set_combobox_selection(self['platform'],
                self.get_attribute_value('platform'))
        self['platform'].set_sensitive(sensitive)

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        self.set_entry_attribute(widget, 'name')

    def on_description_changed(self, widget):
        """
        Signal handler associated with the description text input
        """
        self.set_entry_attribute(widget, 'description')

    def on_domain_changed(self, widget):
        """
        Signal handler associated with the domain combobox
        """
        domain_name = self.get_combobox_selection(self['domain'])
        self.set_attribute_value('domain', domain_name )

    def on_platform_changed(self, widget):
        """
        Signal handler associated with the platform combobox
        """
        platform_name = self.get_combobox_selection(self['platform'])
        self.set_attribute_value('platform', platform_name )

    def destroy(self):
        """
        Cleanly destroyes components
        """
        self.get_control_agent().remove_data_changed_listener(self)
        GtkBasePresentationAgent.destroy(self)
