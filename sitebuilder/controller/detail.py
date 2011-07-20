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
        self._mode = mode
        self._configuration = configuration
        self._view = DetailMainView(self)

        for platform in configuration.get_attribute('sites').values():
            slave = DetailSiteController(platform, mode)
            self._view.attach_slave('site_%s' % platform, 'hbox_sites',
                                    slave.get_view())

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        pass

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
        BaseController.__init__(self)
        self._mode = mode
        self._configuration = configuration
        self._view = DetailSiteView(self)
        configuration.add_data_changed_listener(self)

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.notify_data_changed()

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

    def get_attribute_value(self, name):
        """
        Returns a configuration attribute value
        """
        return self._configuration.get_attribute(name).get_value()

    def check_attribute_value(self, name, value):
        """
        Checks if a potential configuration attribute value is valid
        """
        return self._configuration.get_attribute(name).validate(value)

    def set_attribute_value(self, name, value):
        """
        Returns a configuration attribute value
        """
        self._configuration.get_attribute(name).set_value(value)

    def get_platform_name(self):
        """
        Returns platform anme, that is in fact the configuration name
        """
        return self._configuration.get_name()


if __name__ == '__main__':
    config = ConfigurationManager.get_blank_configuration()
    controller = DetailMainController(config, None)
    view = controller.get_view()
    view.get_toplevel().connect("destroy", gtk.main_quit)
    view.show()
    gtk.main()
