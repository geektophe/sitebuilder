#!/usr/bin/env python
"""
Site details related controllers
"""

from sitebuilder.utils.event import Event
from sitebuilder.view.gtk.detail import DetailMainView
from sitebuilder.view.gtk.detail import DetailDatabaseView
from sitebuilder.view.gtk.detail import DetailGeneralView
from sitebuilder.view.gtk.detail import DetailSiteView
from sitebuilder.view.gtk.detail import DetailRepositoryView
from sitebuilder.model.configuration import ConfigurationManager
from sitebuilder.controller.base import BaseController
from sitebuilder.observer.submitaction import SubmitActionListener
from sitebuilder.observer.submitaction import SubmitActionDispatcher
from sitebuilder.observer.cancelaction import CancelActionListener
import gtk

class DetailMainController(BaseController, SubmitActionListener,
                           SubmitActionDispatcher, CancelActionListener):
    """
    Site details main interface's controller
    """

    def __init__(self, configuration, read_only):
        """
        Controller initialization
        """
        BaseController.__init__(self)
        SubmitActionDispatcher.__init__(self)
        self._read_only = read_only
        self._configuration = configuration
        self._view = DetailMainView(self)
        self._view.add_submit_action_activated_listener(self)
        self._view.add_cancel_action_activated_listener(self)
        self._slaves = []

        # Creates general component
        general = configuration.get_attribute('general')
        slave = DetailGeneralController(general, read_only)
        slave.add_validity_changed_listener(self)
        self._slaves.append(slave)
        self._view.attach_slave('general', 'hbox_general',
                                slave.get_view())

        # Creates repository component
        repository = configuration.get_attribute('repository')
        slave = DetailRepositoryController(repository, read_only)
        slave.add_validity_changed_listener(self)
        self._slaves.append(slave)
        self._view.attach_slave('repository', 'hbox_repository',
                                slave.get_view())

        # Creates site components
        for name in ConfigurationManager.get_site_platforms():
            platform = configuration.get_attribute('sites').get_attribute(name)
            slave = DetailSiteController(platform, read_only)
            slave.add_validity_changed_listener(self)
            self._slaves.append(slave)
            self._view.attach_slave('site_%s' % name, 'hbox_sites',
                                    slave.get_view())

        # Creates database components
        for name in ConfigurationManager.get_database_platforms():
            platform = configuration.get_attribute('databases').get_attribute(name)
            slave = DetailDatabaseController(platform, read_only)
            slave.add_validity_changed_listener(self)
            self._slaves.append(slave)
            self._view.attach_slave('database_%s' % name, 'hbox_databases',
                                    slave.get_view())

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation

        As this class is not sensible to DataChanged events (only sub
        components are), because of DataCHangedListener dependcy, this method
        is nulled
        """
        pass

    def validity_changed(self, event=None):
        """
        ValidityChangedListerner trigger mmethod local implementation

        When a sub component has triggerd a state changed event, the mothod
        enbles or disables the view's OK button depending on each component's
        valid flag.
        """
        flag = True

        for slave in self._slaves:
            flag = flag and slave.get_validity_flag()

        self._view.set_submit_state(flag)

    def submit_action_activated(self, event=None):
        """
        SubmitActionActivatedListerner trigger mmethod local implementation
        """
        self.notify_submit_action_activated(Event(self._configuration))
        self.destroy()

    def cancel_action_activated(self, event=None):
        """
        SubmitActionActivatedListerner trigger mmethod local implementation
        """
        self.destroy()

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

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Destroyes slave components
        for slave in self._slaves:
            slave.destroy()

        # Clears listeners lists
        self.clear_data_changed_listeners()
        self.clear_validity_changed_listeners()
        self.clear_submit_action_activated_listeners()

        # Destroyes view
        self.get_view().destroy()


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

    def data_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.notify_data_changed(event)

    def validity_changed(self, event=None):
        """
        DataChangedListerner trigger mmethod local implementation
        """
        self.notify_validity_changed(event)

    def get_validity_flag(self):
        """
        Returns component's valididty flag
        """
        return self._view.get_validity_flag()

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

    def destroy(self):
        """
        Cleanly destroyes all components
        """
        # Unsubscribes from configuration data changed events
        self._configuration.remove_data_changed_listener(self)

        # Clears listeners lists
        self.clear_data_changed_listeners()
        self.clear_validity_changed_listeners()

        # Destroyes view
        self.get_view().destroy()


class DetailSiteController(DetailComponentController):
    """
    Site sub component controller
    """

    def __init__(self, configuration, read_only=False):
        DetailComponentController.__init__(self, configuration, read_only)
        self._view = DetailSiteView(self)
        self._view.add_validity_changed_listener(self)


class DetailDatabaseController(DetailComponentController):
    """
    Database sub component controller
    """

    def __init__(self, configuration, read_only=False):
        DetailComponentController.__init__(self, configuration, read_only)
        self._view = DetailDatabaseView(self)
        self._view.add_validity_changed_listener(self)


class DetailRepositoryController(DetailComponentController):
    """
    Repository sub component controller
    """

    def __init__(self, configuration, read_only=False):
        DetailComponentController.__init__(self, configuration, read_only)
        self._view = DetailRepositoryView(self)
        self._view.add_validity_changed_listener(self)


class DetailGeneralController(DetailComponentController):
    """
    Repository sub component controller
    """

    def __init__(self, configuration, read_only=False):
        DetailComponentController.__init__(self, configuration, read_only)
        self._view = DetailGeneralView(self)
        self._view.add_validity_changed_listener(self)

if __name__ == '__main__':
    config = ConfigurationManager.get_blank_configuration()
    controller = DetailMainController(config, False)
    view = controller.get_view()
    view.get_toplevel().connect("destroy", gtk.main_quit)
    view.show()
    gtk.main()
