#!/usr/bin/env python
"""
Site editing interface. Supports Create, View and Update modes.
"""

from sitebuilder.utils.parameters import GLADE_BASEDIR
from sitebuilder.presentation.gtk.base import GtkBasePresentation
import gtk

class SitePresentationMain(GtkBasePresentation):
    """
    Main site add/edit/view interface.

    The interface design is loaded from a glade file.
    """

    GLADE_FILE = "%s/%s" % (GLADE_BASEDIR, 'edit.glade')

    def __init__(self, control, mode):
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
        GtkBasePresentation.__init__(self, 'site', control)

        sites_container = self['hbox_sites']
        for platform in ('prod', 'test', 'dev'):
            pass

        self['main'].connect("destroy", gtk.main_quit)
        self['main'].show()

if __name__ == "__main__":
    edit = SitePresentationMain(None, None)
    gtk.main()
