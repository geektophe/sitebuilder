#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.utils.observer import DataChangedListener
from sitebuilder.view.gtk.base import GtkBaseView
from sitebuilder.model.configuration import ConfigurationManager

class DetailMainView(GtkBaseView):
    """
    DetailMainView site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit.glade')

    def __init__(self, controller):
        """
        Class initialization.

        The mandatory mode parameter defines whether the view mode to be used.
        Allowed mode values are add, edit, view.

        - In add mode, the widgets are set in intearcative mode, and a blank
        configuration is used.

        - In edit mode, the widgets are set in interacative mode, and
        configuration loaded from the database is used to fill the widgets.

        - In view mode, the widgets are set non interactive, and
        configuration loaded from the database is used to fill the widgets.
        """
        GtkBaseView.__init__(self, 'main', controller)

    def set_ok_state(self, flag):
        """
        Enables or disabled OK button depending on flag state
        """
        self['ok'].set_sensitive(flag)


class DetailSiteView(GtkBaseView, DataChangedListener):
    """
    Detail site view composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_site.glade')

    def __init__(self, controller):
        """
        Class initialization.
        """
        GtkBaseView.__init__(self, 'site', controller)

        # Sets widget title
        self['label_site'].set_markup(
            "<b>%s site</b>" % controller.get_platform_name().capitalize())

        # Sets widgets signal handlers
        #self._builder.connect_signals(self)
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['proxied'].connect('toggled', self.on_proxied_toggled)
        self['maintenance'].connect('toggled', self.on_maintenance_toggled)
        self['name_cus'].connect('toggled', self.on_name_cus_toggled)
        self['name_def'].connect('toggled', self.on_name_def_toggled)
        self['name'].connect('changed', self.on_name_changed)
        self['template'].connect('changed', self.on_template_changed)
        self['domain'].connect('changed', self.on_domain_changed)

        # Loads comboboxes items
        self.set_combobox_items(self['template'],
                ConfigurationManager.get_site_templates())
        self.set_combobox_items(self['domain'],
                ConfigurationManager.get_site_domains())

        # Loads widgets data from controller
        self.load_widgets_data()

        # Listens data changed events from from controller
        controller.add_data_changed_listener(self)

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the controller
        """
        return self._controller.get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the controller
        """
        self._controller.set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates view widgets based on configuraton settings
        """
        enabled = self.get_attribute_value('enabled')
        done = self.get_attribute_value('done')
        read_only = self._controller.get_read_only_flag()
        sensitive = enabled and not done and not read_only

        maintenance = self.get_attribute_value('maintenance')
        name = self.get_attribute_value('name')

        # Loads enabled checkbox state
        self['enabled'].set_active(enabled)
        self['enabled'].set_sensitive(not done and not read_only)

        # Loads proxied checkbox state (may not be defined in model)
        try:
            proxied = self.get_attribute_value('proxied')
            self['proxied'].set_active(proxied)
            # Proxied should be changeable even if site is in done state
            self['proxied'].set_sensitive(enabled and not read_only)
        except AttributeError:
            self['proxied'].set_sensitive(False)

        # Loads maintenance checkbox state
        self['maintenance'].set_active(maintenance)
        # Maintenance should be changeable even if site is in done state
        self['maintenance'].set_sensitive(enabled and not read_only)

        # Loads site name, and sets appropriate state on name related widgets
        if name == '__DEFAULT__':
            self['name_def'].set_active(True)
            # Disabled to prevent name input deletion if default name is clicked
            #self['name'].set_text('')
        else:
            self['name_cus'].set_active(True)
            self['name'].set_text(name)

        self['name_def'].set_sensitive(sensitive)
        self['name_cus'].set_sensitive(sensitive)
        self['name'].set_sensitive(sensitive and name != '__DEFAULT__')

        # Loads template combobox selected option
        self.set_combobox_selection(self['template'],
                self.get_attribute_value('template'))
        self['template'].set_sensitive(sensitive)

        # Loads domain combobox selected option
        self.set_combobox_selection(self['domain'],
                self.get_attribute_value('domain'))
        self['domain'].set_sensitive(sensitive)

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled checkbox
        """
        enabled = self['enabled'].get_active()
        self.set_attribute_value('enabled', enabled)

    def on_proxied_toggled(self, widget):
        """
        Signal handler associated with the proxied checkbox
        """
        proxied = self['proxied'].get_active()
        self.set_attribute_value('proxied', proxied)

    def on_maintenance_toggled(self, widget):
        """
        Signal handler associated with the maintenance checkbox
        """
        maintenance = self['maintenance'].get_active()
        self.set_attribute_value('maintenance', maintenance)

    def on_name_def_toggled(self, widget):
        """
        Signal handler associated with the named_def radio button
        """
        if widget.get_active() == True:
            self.set_attribute_value('name', '__DEFAULT__')

    def on_name_cus_toggled(self, widget):
        """
        Signal handler associated with the named_cus radio button
        """
        self['name'].set_sensitive(True)

    def on_name_changed(self, widget):
        """
        Signal handler associated with the name text input
        """
        self.set_entry_attribute(widget, 'name')

    def on_template_changed(self, widget):
        """
        Signal handler associated with the template combobox
        """
        template_name = self.get_combobox_selection(self['template'])
        self.set_attribute_value('template', template_name )

    def on_domain_changed(self, widget):
        """
        Signal handler associated with the domain combobox
        """
        domain_name = self.get_combobox_selection(self['domain'])
        self.set_attribute_value('domain', domain_name )


class DetailDatabaseView(GtkBaseView, DataChangedListener):
    """
    Detail database view composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_db.glade')

    def __init__(self, controller):
        """
        Class initialization.
        """
        GtkBaseView.__init__(self, 'database', controller)

        # Sets widget title
        self['label_database'].set_markup(
            "<b>%s database</b>" % controller.get_platform_name().capitalize())

        # Sets widgets signal handlers
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['name'].connect('changed', self.on_name_changed)
        self['username'].connect('changed', self.on_username_changed)
        self['password'].connect('changed', self.on_password_changed)
        self['type'].connect('changed', self.on_type_changed)

        # Loads comboboxes items
        self.set_combobox_items(self['type'],
                ConfigurationManager.get_database_types())

        # Loads widgets data from controller
        self.load_widgets_data()

        # Listens data changed events from from controller
        controller.add_data_changed_listener(self)

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the controller
        """
        return self._controller.get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the controller
        """
        self._controller.set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates view widgets based on configuraton settings
        """
        enabled = self.get_attribute_value('enabled')
        done = self.get_attribute_value('done')
        read_only = self._controller.get_read_only_flag()
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


class DetailRepositoryView(GtkBaseView, DataChangedListener):
    """
    Detail repository view composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_repo.glade')

    def __init__(self, controller):
        """
        Class initialization.
        """
        GtkBaseView.__init__(self, 'repository', controller)

        # Sets widgets signal handlers
        self['enabled'].connect('toggled', self.on_enabled_toggled)
        self['name'].connect('changed', self.on_name_changed)
        self['type'].connect('changed', self.on_type_changed)

        # Loads comboboxes items
        self.set_combobox_items(self['type'],
                ConfigurationManager.get_repository_types())

        # Loads widgets data from controller
        self.load_widgets_data()

        # Listens data changed events from from controller
        controller.add_data_changed_listener(self)

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the controller
        """
        return self._controller.get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the controller
        """
        self._controller.set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates view widgets based on configuraton settings
        """
        enabled = self.get_attribute_value('enabled')
        done = self.get_attribute_value('done')
        read_only = self._controller.get_read_only_flag()
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


class DetailGeneralView(GtkBaseView, DataChangedListener):
    """
    Detail general view composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_general.glade')

    def __init__(self, controller):
        """
        Class initialization.
        """
        GtkBaseView.__init__(self, 'general', controller)

        # Sets widgets signal handlers
        self['name'].connect('changed', self.on_name_changed)
        self['description'].connect('changed', self.on_description_changed)

        # Loads widgets data from controller
        self.load_widgets_data()

        # Listens data changed events from from controller
        controller.add_data_changed_listener(self)

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.load_widgets_data()

    def get_attribute_value(self, name):
        """
        Returns an attribute value from the controller
        """
        return self._controller.get_attribute_value(name)

    def set_attribute_value(self, name, value):
        """
        Sets an attribute value on the controller
        """
        self._controller.set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates view widgets based on configuraton settings
        """
        read_only = self._controller.get_read_only_flag()
        name = self.get_attribute_value('name')
        description = self.get_attribute_value('description')

        # Loads name entry
        self['name'].set_text(name)
        self['name'].set_sensitive(not read_only)

        # Loads description entry
        self['description'].set_text(description)
        self['description'].set_sensitive(not read_only)

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
