#!/usr/bin/env python
"""
Site details related controllers
"""

from sitebuilder.view.gtk.detail import DetailMainView
from sitebuilder.view.gtk.detail import DetailSiteView
from sitebuilder.view.gtk.detail import DetailDatabaseView
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.controller.base import BaseController
import gtk

class DetailMainController(BaseController):
    """
    Site details main interface's controller
    """

    def __init__(self, configuration, read_only):
        """
        Controller initialization
        """
        BaseController.__init__(self)
        self._read_only = read_only
        self._configuration = configuration
        self._view = DetailMainView(self)

        for name in ConfigurationManager.get_site_platforms():
            platform = configuration.get_attribute('sites').get_attribute(name)
            slave = DetailSiteController(platform, read_only)
            self._view.attach_slave('site_%s' % name, 'hbox_sites',
                                    slave.get_view())

        for name in ConfigurationManager.get_database_platforms():
            platform = configuration.get_attribute('databases').get_attribute(name)
            slave = DetailDatabaseController(platform, read_only)
            self._view.attach_slave('database_%s' % name, 'hbox_databases',
                                    slave.get_view())

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        pass

    def get_read_only_flag(self):
        """
        Returns read only flag
        """
        return self._read_only

    def get_view(self):
        """
        Returns view
        """
        return self._view


class DetailComponentController(BaseController):
    """
    Generic sub component controller
    """

    def __init__(self, configuration, read_only=False):
        """
        Initializes controller.

        The read_only attribute indocates to the view that none of then widgets
        should be sensitive. The user is then not allowed to change any value.
        """
        BaseController.__init__(self)
        self._read_only = read_only
        self._configuration = configuration
        self._view = None
        configuration.add_data_changed_listener(self)

    def data_changed(self):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.notify_data_changed()

    def get_read_only_flag(self):
        """
        Returns read only flag
        """
        return self._read_only

    def get_view(self):
        """
        Returns DetailSiteView view instance
        """
        return self._view

    def get_configuratuon(self):
        """
        Returns configuration instance
        """
        return self._configuration

    def get_attribute_value(self, name):
        """
        Returns a configuration attribute value
        """
        return self._configuration.get_attribute(name).get_value()

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


class DetailSiteController(DetailComponentController):
    """
    Site sub component controller
    """

    def __init__(self, configuration, read_only=False):
        DetailComponentController.__init__(self, configuration, read_only)
        self._view = DetailSiteView(self)


class DetailDatabaseController(DetailComponentController):
    """
    Database sub component controller
    """

    def __init__(self, configuration, read_only=False):
        DetailComponentController.__init__(self, configuration, read_only)
        self._view = DetailDatabaseView(self)


if __name__ == '__main__':
    config = ConfigurationManager.get_blank_configuration()
    controller = DetailMainController(config, False)
    view = controller.get_view()
    view.get_toplevel().connect("destroy", gtk.main_quit)
    view.show()
    gtk.main()
