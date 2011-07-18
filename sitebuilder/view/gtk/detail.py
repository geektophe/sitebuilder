#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.utils.observer import DataChangedListener
from sitebuilder.view.gtk.base import GtkBaseView
import gtk

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


class DetailSiteView(GtkBaseView,DataChangedListener):
    """
    DetailSiteView composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_site.glade')

    def __init__(self, controller):
        """
        Class initialization.
        """
        GtkBaseView.__init__(self, 'site', controller)
        label_site = self['label_site']
        label_site.set_markup("<b>%s site</b>" % \
                            controller.get_platform_name().capitalize())
        self.load_widgets_data()
        controller.add_data_changed_listener(self)
        #self._builder.connect_signals(self)
        enabled = self['enabled']
        name_cus = self['name_cus']
        name_def = self['name_def']
        name = self['name']
        enabled.connect('toggled', self.on_enabled_toggled)
        name_cus.connect('toggled', self.on_name_cus_toggled)
        name_def.connect('toggled', self.on_name_def_toggled)
        name.connect('changed', self.on_name_changed)

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
        return self._controller.set_attribute_value(name, value)

    def load_widgets_data(self):
        """
        Updates view widgets based on configuraton settings
        """
        enabled = self.get_attribute_value('enabled')
        done = self.get_attribute_value('done')
        sensitive = enabled and not done

        maintenance = self.get_attribute_value('maintenance')
        name = self.get_attribute_value('name')

        self['enabled'].set_active(enabled)
        self['enabled'].set_sensitive(not done)

        try:
            proxied = self.get_attribute_value('proxied')
            self['proxied'].set_active(proxied)
            self['proxied'].set_sensitive(enabled)
        except AttributeError:
            self['proxied'].set_sensitive(False)

        self['maintenance'].set_active(maintenance)
        self['maintenance'].set_sensitive(enabled)

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

    def on_enabled_toggled(self, widget):
        """
        Signal handler associated with the enabled check button
        """
        enabled = self['enabled'].get_active()
        self.set_attribute_value('enabled', enabled)

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
        Signal handler associated with the named_text input
        """
        name = widget.get_text()

        try:
            widget.set_tooltip_text('')
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#90EE90'))
            self._controller.set_attribute_value('name', name)
        except AttributeError, e:
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('#FFCCCC'))
            widget.set_tooltip_text(str(e))

