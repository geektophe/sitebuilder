#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.view.gtk.base import GtkBaseView
import gtk

class SiteMainView(GtkBaseView):
    """
    SiteMainView site add/edit/view interface.

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


class SiteSiteView(GtkBaseView):
    """
    SiteSiteView composite widget.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit_site.glade')

    def __init__(self, controller):
        """
        Class initialization.
        """
        GtkBaseView.__init__(self, 'site', controller)
        enabled = self['site_enabled']
        enabled.connect('toggled', self.on_site_enabled_toggled)

    def on_site_enabled_toggled(self, widget):
        print "Site enabled: %s" % widget.get_active()

if __name__ == "__main__":
    edit = SiteMainView(None, None)
    for platform in ('prod', 'test', 'dev'):
        slave = SiteSiteView(None)
        edit.attach_slave('site_%s' % platform, 'hbox_sites', slave)

    edit.get_toplevel().connect("destroy", gtk.main_quit)
    edit.show()
    prod = edit['site_prod']
    gtk.main()
