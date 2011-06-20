#!/usr/bin/env python
"""
Site related controllers
"""

from sitebuilder.view.gtk.site import SiteMainView, SiteSiteView
import gtk

class SiteMainController(object):
    """
    Site main interface's controller
    """

    def __init__(self, configuration, mode):
        """
        Controller initialization
        """
        self._view = SiteMainView(self)
        self._mode = mode

        for platform in ('prod', 'test', 'dev'):
            slave = SiteSiteController(configuration, mode)
            self._view.attach_slave('site_%s' % platform, 'hbox_sites',
                                    slave.get_view())

    def get_mode(self):
        """
        Returns editting mode
        """
        return self._mode

    def get_view(self):
        """
        Returns view
        """
        return self._view


class SiteSiteController(object):
    """
    Site widget's controller
    """
    def __init__(self, configuration, mode):
        self._view = SiteSiteView(self)
        self._mode = mode

    def get_mode(self):
        """
        Returns editting mode
        """
        return self._mode

    def get_view(self):
        """
        Returns view
        """
        return self._view



if __name__ == '__main__':
    controller = SiteMainController(None, None)
    view = controller.get_view()
    view.get_toplevel().connect("destroy", gtk.main_quit)
    view.show()
    gtk.main()
