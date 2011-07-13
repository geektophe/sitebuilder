#!/usr/bin/env python
"""
Site details related controllers
"""

from sitebuilder.view.gtk.detail import DetailMainView, DetailSiteView
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.controller.base import BaseController
import gtk

class DetailMainController(BaseController):
    """
    Site details main interface's controller
    """

    def __init__(self, configuration, mode):
        """
        Controller initialization
        """
        BaseController.__init__(self)
        self._view = DetailMainView(self)
        self._mode = mode
        self._configuration = configuration

        for platform in configuration.get_attribute('sites').values():
            slave = DetailSiteController(platform, mode)
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


class DetailSiteController(BaseController):
    """
    Site widget's controller
    """
    def __init__(self, configuration, mode):
        self._view = DetailSiteView(self)
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

    def get_site_enbled(self):
        """
        Returns site's enabled flag
        """
        return self._view



if __name__ == '__main__':
    configuration = ConfigurationManager.get_blank_configuration()
    controller = DetailMainController(configuration, None)
    view = controller.get_view()
    view.get_toplevel().connect("destroy", gtk.main_quit)
    view.show()
    gtk.main()
